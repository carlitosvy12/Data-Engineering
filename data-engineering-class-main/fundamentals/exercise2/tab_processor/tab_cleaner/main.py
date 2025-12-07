
import os
import re
import logging as log
import datetime
from utils.string_mapping import MAPPING


INPUT_DIRECTORY = "./tab_processor/files/songs/"

OUTPUT_DIRECTORY = "./tab_processor/files/cleaned/"
LOGS_DIRECTORY = "./tab_processor/logs/"
CATALOG_DIRECTORY = f"{INPUT_DIRECTORY}catalogs/"

ROOT = "https://acordes.lacuerda.net"
URL_ARTIST_INDEX = "https://acordes.lacuerda.net/tabs/"
MIN_LINES = 5
SONG_VERSION = 0
INDEX = "abcdefghijklmnopqrstuvwxyz#"

dir_list = [] 

# --- Logging config ---
logger = log.getLogger(__name__)

log.basicConfig(
    filename=f"{LOGS_DIRECTORY}cleaner.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)




def list_files_recursive(path):
    
    valid_files = []

    for root, dirs, files in os.walk(path):
        
        root_norm = root.replace("\\", "/").lower()

        
        if "/cleaned" in root_norm:
            continue
        if "/validations" in root_norm:
            continue
        if "/lyrics" in root_norm:
            continue
        if "/results" in root_norm:
            continue

        
        if "/songs/" not in root_norm:
            continue

        
        for f in files:
            if f.lower().endswith(".txt"):
                valid_files.append(os.path.join(root, f))

    return valid_files



def remove_email_sentences(text: str):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    sentence_pattern = r"[\n^.!?]*" + email_pattern + r"[^.!?]*[.!?\n]"
    return re.sub(sentence_pattern, "", text)


def apply_format_rules(text: str):
    formatted_text = remove_email_sentences(text)

    for key, value in MAPPING.items():
        formatted_text = re.sub(
            key, value, formatted_text, flags=re.DOTALL | re.IGNORECASE
        )

    return formatted_text


def main():

    print("Starting cleaner...")
    start_time = datetime.datetime.now()
    log.info(f"Cleaner started at {start_time}")

    cleaned = 0

    files_to_clean = list_files_recursive(INPUT_DIRECTORY)

    for file_path in files_to_clean:

        log.info(f"Processing file -> {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        if text.count("\n") < MIN_LINES:
            log.info("File too small. Skipping.")
            continue

        formatted_text = apply_format_rules(text)

        
        file_path_norm = file_path.replace("\\", "/")
        input_norm = INPUT_DIRECTORY.replace("\\", "/")

        
        relative_path = os.path.relpath(file_path_norm, input_norm).replace("\\", "/")

        
        if relative_path.startswith("songs/"):
             relative_path = relative_path[len("songs/"):]


        output_file = os.path.join(OUTPUT_DIRECTORY, relative_path)

        output_dir = os.path.dirname(output_file)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print("INFO: created directory", output_dir)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(formatted_text)

        cleaned += 1
        print(cleaned, "--", os.path.basename(output_file), "CREATED!!")

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    log.info(f"Cleaner ended at {end_time}")
    print(f"Cleaner finished in {duration.total_seconds()} seconds")


if __name__ == "__main__":
    main()
