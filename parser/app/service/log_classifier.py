import re
import datetime
import logging
from collections import defaultdict
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LogClassifier:
    def __init__(self, request_threshold=100, interval_threshold=2, error_threshold=20):
        # Classifier configuration
        self.request_threshold = request_threshold
        self.interval_threshold = interval_threshold
        self.error_threshold = error_threshold
        
        # Store extracted IP features
        self.ip_features = {}

    def parse_log_line(self, line):
        """
        Parses a single log line using regex.
        Returns a dictionary with extracted fields or None if parsing fails.
        """
        pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] '
            r'"(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" '
            r'(?P<status>\d+) (?P<size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
        )
        match = pattern.match(line)
        if match:
            data = match.groupdict()
            try:
                # Convert timestamp to datetime object
                timestamp = datetime.datetime.strptime(data['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
                data['timestamp'] = timestamp
                return data
            except ValueError as e:
                logging.warning(f"Timestamp parsing error: {e}")
                return None
        return None

    def train_model(self, log_file_path):
        """
        Reads a log file, extracts request data, and computes per-IP behavioral features.
        """
        ip_data = defaultdict(lambda: {
            'timestamps': [],
            'urls': set(),
            'user_agents': set(),
            'status_counts': defaultdict(int)
        })

        try:
            with open(log_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parsed = self.parse_log_line(line)
                    if parsed:
                        ip = parsed['ip']
                        ip_data[ip]['timestamps'].append(parsed['timestamp'])
                        ip_data[ip]['urls'].add(parsed['url'])
                        ip_data[ip]['user_agents'].add(parsed['user_agent'])
                        ip_data[ip]['status_counts'][parsed['status']] += 1

            # Feature extraction for each IP
            for ip, data in ip_data.items():
                timestamps = sorted(data['timestamps'])
                if len(timestamps) < 2:
                    continue

                # Calculate time intervals between consecutive requests
                intervals = [
                    (timestamps[i+1] - timestamps[i]).total_seconds()
                    for i in range(len(timestamps)-1)
                ]

                request_count = len(timestamps)
                avg_interval = statistics.mean(intervals) if intervals else float('inf')
                unique_urls = len(data['urls'])

                # Count error responses (4xx & 5xx status codes)
                error_count = sum(
                    count for code, count in data['status_counts'].items()
                    if code.startswith('4') or code.startswith('5')
                )

                # Store extracted features
                self.ip_features[ip] = {
                    'request_count': request_count,
                    'avg_interval': avg_interval,
                    'unique_urls': unique_urls,
                    'error_count': error_count
                }

            logging.info("Model training completed successfully.")

        except Exception as e:
            logging.error(f"Error during training: {e}")

    def predict_suspected_ips(self):
        """
        Predicts suspected IPs based on request frequency, timing, and error patterns.
        Returns a list of suspected IP addresses.
        """
        suspected = []
        for ip, feat in self.ip_features.items():
            if (
                feat['request_count'] > self.request_threshold and
                feat['avg_interval'] < self.interval_threshold or
                feat['error_count'] > self.error_threshold
            ):
                suspected.append(ip)

        logging.info(f"Detected {len(suspected)} suspected IP(s).")
        return suspected

    def get_ip_features(self):
        """
        Returns the computed features for all IPs.
        """
        return self.ip_features
