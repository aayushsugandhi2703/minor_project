import os
import re
import json
import requests

def fetch_store_file(link):

    """Fetches log data from the given URL and saves it to a local file."""
    try:
        response = requests.get(link, timeout=10)  
        response.raise_for_status()  # Raise an error for 4xx and 5xx status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    directory = 'log_files'
    os.makedirs(directory, exist_ok=True)  # Creates directory if it doesn't exist
    file_path = os.path.join(directory, "logs.txt")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
    except OSError as e:
        print(f"Error writing to file: {e}")

def save_parse_logs_json():

    """Parses logs from 'logs.txt' and saves them as JSON in 'parselog.json'."""

    log_file_path = 'log_files/logs.txt'
    output_file_path = 'log_files/parselog.json'

    if not os.path.exists(log_file_path):
        print("Error: Log file does not exist.")
        return

    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"')

    parsed_data = []

    with open(log_file_path, 'r', encoding='utf-8') as file:
        for log in file:
            match = pattern.search(log)  # Check if the log entry matches the pattern
            if match:
                parsed_data.append(match.groupdict())

    if parsed_data:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(parsed_data, json_file, indent=4)
        except OSError as e:
            print(f"Error writing to file: {e}")
    else:
        print("No valid log entries found.")
