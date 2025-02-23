import os
import re
import json
import requests

def fetch(link):

#Fetches log data from the given URL and saves it to a local file.
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
            json.dump(response.json(), file, indent=4)
        print(f"Logs Uploaded")
    except OSError as e:
        print(f"Error writing to file: {e}")

def parse_logs():
#Parses the log data from the local file
    log_file = 'log_files/logs.txt'

    if not os.path.exists(log_file):
        print("Error: Log file does not exist.")
        return []  # Exit function early

    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            logs = json.load(file)  # Load logs from JSON file
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return []

    log_list = []
    
    # Compiled regex for efficiency
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"')

    for log in logs:
        for match in pattern.finditer(log):  # Using finditer() for multiple matches
            log_list.append(match.groupdict())  # Extract dictionary of matched fields

    return log_list