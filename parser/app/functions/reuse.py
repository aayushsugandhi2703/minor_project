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
    except OSError as e:
        print(f"Error writing to file: {e}")