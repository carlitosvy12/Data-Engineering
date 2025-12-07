
import os
import click
import re
import logging as log
import datetime
import shutil


INPUT_DIRECTORY = "./tab_processor/files/"
CLEANED_DIRECTORY = "./tab_processor/files/cleaned"
OUTPUT_DIRECTORY_OK = "./tab_processor/files/validations/ok"
OUTPUT_DIRECTORY_KO = "./tab_processor/files/validations/ko"

ROOT = "https://acordes.lacuerda.net"
URL_ARTIST_INDEX = "https://acordes.lacuerda.net/tabs/"
SONG_VERSION = 0
INDEX = "abcdefghijklmnopqrstuvwxyz#"

dir_list = []

def validate_song_format(song):
    """Validates if the song follows a basic expected format."""
    pattern = r"((?:[A-Z]+\s+)*\n.+)+"
    match = re.fullmatch(pattern, song, flags=re.DOTALL)
    return bool(match)


def has_valid_chord(song):
    """Checks if the tab contains at least one valid chord."""
    chord_pattern = r'\b[A-G][#b]?(m|maj7|sus2|sus4|dim|7|9)?\b'
    return re.search(chord_pattern, song) is not None

def has_meaningful_line(song):
    """Returns True if there is a line with more than 10 characters."""
    for line in song.splitlines():
        if len(line.strip()) > 10:
            return True
    return False



def list_files_recursive(path: str):
    """Lists all files in a directory recursively."""
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            dir_list.append(full_path)

    return dir_list


@click.command()
@click.option(
    "--init",
    "-i",
    is_flag=True,
    default=False,
    help="If present, deletes old validations and starts fresh.",
)
def main(init):

    start_time = datetime.datetime.now()
    print("Starting validator...")

    # Reset validated output folders
    if init:
        if os.path.exists(OUTPUT_DIRECTORY_OK):
            shutil.rmtree(OUTPUT_DIRECTORY_OK)
        if os.path.exists(OUTPUT_DIRECTORY_KO):
            shutil.rmtree(OUTPUT_DIRECTORY_KO)
        print("Validation folders reset.")

    OK = 0
    KO = 0

    for file_path in list_files_recursive(CLEANED_DIRECTORY):

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        validated = (
          validate_song_format(text)
          and (has_valid_chord(text) or has_meaningful_line(text))
        )

        
        filename = os.path.basename(file_path)

        if validated:
            output_file = os.path.join(OUTPUT_DIRECTORY_OK, filename)
            OK += 1
        else:
            output_file = os.path.join(OUTPUT_DIRECTORY_KO, filename)
            KO += 1

        
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created directory: {output_dir}")

        
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)
            print(f"OK={OK}  KO={KO}  →  {filename} saved")

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print(f"Validator finished in {duration.total_seconds()} seconds")


if __name__ == "__main__":
    main()
