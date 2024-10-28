
import json
import os
import time
import re
import glob
import yaml
from datetime import datetime

DEFAULT_CONFIG_DIR: str = '../config.yaml' # Google drive: "/content/drive/MyDrive/cfr2sbvr/config.yaml

def get_next_filename(file_dir: str, file_prefix: str, extension: str) -> str:
    """
    Generates the next filename in a sequence based on existing files in a directory,
    considering the file extension.

    The filename format is: `{file_prefix}-{YYYY-MM-DD}-{N}.{extension}`,
    where `N` is an incrementing integer for files with the same date.

    Args:
        file_dir (str): The directory where the files are stored.
        file_prefix (str): The prefix used in the filenames.
        extension (str): The file extension (e.g., 'json', 'txt').

    Returns:
        str: The full path to the next filename in the sequence.

    Example:
        next_file = get_next_filename(DEFAULT_CHECKPOINTS_DIR, 'documents', 'json')
        print(next_file)
        # Output might be: ../checkpoints/documents-2024-10-19-5.json
    """
    today_str: str = datetime.today().strftime('%Y-%m-%d')
    path: str = file_dir

    # Ensure the directory exists
    if not os.path.exists(path):
        os.makedirs(path)

    files = os.listdir(path)

    # Create the pattern dynamically using file_prefix and extension
    pattern = re.compile(
        r'^' + re.escape(file_prefix) + r'-(\d{4}-\d{2}-\d{2})-(\d+)\.' + re.escape(extension) + r'$'
    )

    file_info_list = []

    for filename in files:
        match = pattern.match(filename)
        if match:
            date_str: str = match.group(1)
            number: int = int(match.group(2))
            file_info_list.append({'filename': filename, 'date': date_str, 'number': number})

    if file_info_list:
        # Sort by date and number in descending order
        sorted_files = sorted(
            file_info_list,
            key=lambda x: (x['date'], x['number']),
            reverse=True
        )

        latest_file_info = sorted_files[0]
        latest_date: str = latest_file_info['date']
        latest_number: int = latest_file_info['number']

        if latest_date == today_str:
            new_number: int = latest_number + 1
        else:
            new_number = 1
    else:
        new_number = 1

    new_filename: str = f'{file_prefix}-{today_str}-{new_number}.{extension}'
    new_filepath: str = os.path.join(path, new_filename)

    return new_filepath


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
