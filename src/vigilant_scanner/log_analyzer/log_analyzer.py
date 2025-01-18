import re
import os

# Define patterns for malicious activities
MALICIOUS_PATTERNS = {
    "XSS": re.compile(r"<script>|onerror=|document\.cookie", re.IGNORECASE),
    "SQL Injection": re.compile(r"(UNION SELECT|SELECT.*FROM|DROP TABLE|OR 1=1|--)", re.IGNORECASE),
    "Directory Traversal": re.compile(r"\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c", re.IGNORECASE),
    "Remote Code Execution": re.compile(r"(wget|curl|bash -i|nc -e|/bin/sh)", re.IGNORECASE),
    "Brute Force": re.compile(r"(Failed login attempt|Invalid password)", re.IGNORECASE),
    "File Upload Exploit": re.compile(r"(\.php|\.exe|\.sh)$", re.IGNORECASE),
    "HTTP Method Abuse": re.compile(r"(TRACE|OPTIONS|CONNECT)", re.IGNORECASE),
}


def scan_log_file(log_file):
    """
    Scan a single log file for malicious activity patterns.

    Args:
        log_file (str): Path to the log file.

    Returns:
        dict: Detected malicious activities and their counts.
    """
    detections = {pattern_name: [] for pattern_name in MALICIOUS_PATTERNS}

    try:
        with open(log_file, "r") as file:
            for line_number, line in enumerate(file, start=1):
                for pattern_name, pattern in MALICIOUS_PATTERNS.items():
                    if pattern.search(line):
                        detections[pattern_name].append((line_number, line.strip()))
    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
    except Exception as e:
        print(f"An error occurred while scanning {log_file}: {e}")

    return detections


def scan_directory_for_logs(directory):
    """
    Scan all .log files in the provided directory for malicious patterns.

    Args:
        directory (str): Path to the directory containing log files.
    """
    if not os.path.isdir(directory):
        print(f"Invalid directory: {directory}")
        return

    print(f"Scanning directory: {directory}")
    log_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".log")]

    if not log_files:
        print("No .log files found in the directory.")
        return

    for log_file in log_files:
        print(f"\nScanning file: {log_file}")
        results = scan_log_file(log_file)

        any_detection = False
        for pattern_name, matches in results.items():
            if matches:
                any_detection = True
                print(f"\n[Detected: {pattern_name}]")
                for line_number, line_content in matches:
                    print(f"  Line {line_number}: {line_content}")

        if not any_detection:
            print("No malicious activity detected in this file.")
