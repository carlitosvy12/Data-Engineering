import os

CLEANED_DIR = "./tab_processor/files/cleaned/abel_pintos"
OK_DIR = "./tab_processor/files/validations/ok"
KO_DIR = "./tab_processor/files/validations/ko"


def count_files(path):
    """Count only files, ignoring directories."""
    if not os.path.exists(path):
        return 0
    return sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))


def main():
    cleaned = count_files(CLEANED_DIR)
    ok = count_files(OK_DIR)
    ko = count_files(KO_DIR)

    print("======= RESULTS =======")
    print(f"Cleaned files: {cleaned}")
    print(f"Validations OK: {ok}")
    print(f"Validations KO: {ko}")
    print("========================")


if __name__ == "__main__":
    main()
