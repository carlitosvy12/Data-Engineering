import os
import re

OK_DIR = "./tab_processor/files/validations/ok"


def remove_chords(text):
    pattern = r"\b[A-G][#b]?\w*\b"
    return re.sub(pattern, "", text)



def process_ok_files():
    """Generates a lyrics-only version for each successfully validated file."""
    if not os.path.exists(OK_DIR):
        print("OK directory not found.")
        return

    for f in os.listdir(OK_DIR):

        full_path = os.path.join(OK_DIR, f)

        if not os.path.isfile(full_path):
            continue  # ignore directories

        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Remove chords
        lyrics_only = remove_chords(content)

        # New filename
        base, ext = os.path.splitext(f)
        new_name = f"{base}_lyrics{ext}"
        new_path = os.path.join(OK_DIR, new_name)

        # Save lyrics-only file
        with open(new_path, "w", encoding="utf-8") as file:
            file.write(lyrics_only)

        print(f"Created: {new_name}")


def main():
    print("Generating lyrics-only files...")
    process_ok_files()
    print("Done.")


if __name__ == "__main__":
    main()
