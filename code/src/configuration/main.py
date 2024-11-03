
import os
import json
import time
import re
import glob
import yaml
from datetime import datetime
from pathlib import Path

DEFAULT_CONFIG_DIR: str = '../config.yaml'  # Google drive: "/content/drive/MyDrive/cfr2sbvr/config.yaml"

def _get_sorted_file_info(file_dir: str, file_prefix: str, extension: str):
    """
    Helper function to retrieve and sort file information based on a specific prefix and extension.

    Args:
        file_dir (str): Directory to search for files.
        file_prefix (str): Prefix for the filenames.
        extension (str): File extension.

    Returns:
        list: Sorted list of file information dictionaries containing 'filename', 'date', and 'number' keys.
    """
    path = Path(file_dir)
    path.mkdir(parents=True, exist_ok=True)

    files = list(path.glob(f"{file_prefix}-*.{extension}"))
    file_info_list = []

    pattern = re.compile(rf'^{file_prefix}-(\d{{4}}-\d{{2}}-\d{{2}})-(\d+)\.{extension}$')
    for filepath in files:
        match = pattern.match(filepath.name)
        if match:
            date_str = match.group(1)
            number = int(match.group(2))
            file_info_list.append({'filename': filepath.name, 'date': date_str, 'number': number})

    return sorted(file_info_list, key=lambda x: (x['date'], x['number']), reverse=True)

def get_next_filename(file_dir: str, file_prefix: str, extension: str) -> str:
    """
    Generates the next filename in a sequence based on existing files in a directory,
    considering the file extension.

    The filename format is: `{file_prefix}-{YYYY-MM-DD}-{N}.{extension}`,
    where `N` is an incrementing integer for files with the same date.
    """
    today_str = datetime.today().strftime('%Y-%m-%d')
    sorted_files = _get_sorted_file_info(file_dir, file_prefix, extension)

    if sorted_files and sorted_files[0]['date'] == today_str:
        new_number = sorted_files[0]['number'] + 1
    else:
        new_number = 1

    new_filename = f'{file_prefix}-{today_str}-{new_number}.{extension}'
    return str(Path(file_dir) / new_filename)

def get_last_filename(file_dir: str, file_prefix: str, extension: str) -> str:
    """
    Retrieves the most recent filename based on the highest date and sequence number
    for files with a specific prefix and extension in the specified directory.
    """
    sorted_files = _get_sorted_file_info(file_dir, file_prefix, extension)
    if sorted_files:
        return str(Path(file_dir) / sorted_files[0]['filename'])
    return None

# Load the YAML config file
def load_config(config_file: str = None):
    if config_file is None:
        config_file = DEFAULT_CONFIG_DIR
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    except yaml.YAMLError as exc:
        raise ValueError(f"Error parsing YAML file {config_file}: {exc}")

    # Ensure config structure is correct
    if "LLM" not in config or "DEFAULT_CHECKPOINT_DIR" not in config:
        raise ValueError("Required configuration keys are missing in the config file.")

    # Set the OpenAI API key from environment variable if it's not set in config
    config["LLM"]["OPENAI_API_KEY"] = os.getenv(
        "OPENAI_API_KEY", config["LLM"].get("OPENAI_API_KEY")
    )

    # Dynamically set checkpoint and report files using the get_next_filename function
    config["DEFAULT_CHECKPOINT_FILE"] = get_next_filename(
        config["DEFAULT_CHECKPOINT_DIR"], "documents", "json"
    )
    config["DEFAULT_EXTRACTION_REPORT_FILE"] = get_next_filename(
        config["DEFAULT_OUTPUT_DIR"], "extraction_report", "html"
    )

    return config
