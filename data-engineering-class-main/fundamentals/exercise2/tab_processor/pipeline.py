import subprocess
import logging
import datetime
import os

# Paths
LOG_DIR = "./tab_processor/logs"
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

MODULES = [
    "tab_processor/scrapper/main.py",
    "tab_processor/tab_cleaner/main.py",
    "tab_processor/tab_validator/main.py",
    "tab_processor/lyrics.py",
    "tab_processor/results.py",
    "tab_processor/insights.py",
]


def setup_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        filename=LOG_FILE,
        filemode="w",
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


def run_module(path):
    """Executes a python module and logs success or failure."""
    try:
        logging.info(f"Starting module: {path}")
        result = subprocess.run(
            ["python", path], capture_output=True, text=True
        )

        # Log standard output
        if result.stdout:
            logging.info(f"OUTPUT ({path}):\n{result.stdout}")

        # Log errors (if any)
        if result.stderr:
            logging.error(f"ERROR ({path}):\n{result.stderr}")

        # If non-zero exit code → failure
        if result.returncode != 0:
            logging.error(f"Module FAILED: {path}")
            return False

        logging.info(f"Module completed successfully: {path}")
        return True

    except Exception as e:
        logging.exception(f"Exception while running module {path}: {e}")
        return False


def main():
    setup_logger()

    logging.info("===== PIPELINE STARTED =====")
    start = datetime.datetime.now()

    for module in MODULES:
        ok = run_module(module)
        if not ok:
            logging.error(f"Pipeline stopped due to failure in: {module}")
            break

    end = datetime.datetime.now()
    duration = end - start

    logging.info(f"===== PIPELINE FINISHED after {duration} =====")


if __name__ == "__main__":
    main()
