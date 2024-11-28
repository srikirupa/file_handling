import logging
import csv
from collections import defaultdict
from datetime import datetime
import pandas as pd
import os

filename = '/usr/local/google/home/srikirupa/Downloads/error_log/error_log_data.csv'

def setup_logger():
    """Sets up the logger with the required configuration."""
    logging.basicConfig(
        filename='error_log_analysis.log',  # Log file name
        level=logging.DEBUG,               # The minimum level of severity to log
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        datefmt='%Y-%m-%d %H:%M:%S'         # Timestamp format
    )

def read_log_file(filename):
    if not os.path.exists(filename):
        logging.error(f"The file {filename} was not found.")
        return None

    try:
        logs = pd.read_csv(filename)
    except FileNotFoundError:
        logging.error(f"The file {filename} was not found.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

    return logs

def parse_logs(logs):
    error_trends = defaultdict(int)
    severity_trends = defaultdict(int)
    resolution_times = []
    user_error_count = defaultdict(int)

    for index, log in logs.iterrows():
        try:
            error_code = log['error_code']
            error_trends[error_code] += 1

            severity = log['severity']
            severity_trends[severity] += 1

            if str(log['resolution_time']).strip().isdigit():
                resolution_times.append(int(log['resolution_time']))

            user_id = log['user_id']
            user_error_count[user_id] += 1

        except KeyError as e:
            logging.warning(f"Missing expected field {e} in log entry.")
        except ValueError as e:
            logging.warning(f"Invalid value found in log entry: {e}")

    return error_trends, severity_trends, resolution_times, user_error_count

def calculate_trends(error_trends, severity_trends, resolution_times, user_error_count):
    """Calculates and logs trend analysis results."""
    
    logging.info("\nTop 5 Error Codes:")
    sorted_error_codes = sorted(error_trends.items(), key=lambda x: x[1], reverse=True)
    for code, count in sorted_error_codes[:5]:
        logging.info(f"{code}: {count} occurrences")

    logging.info("\nSeverity Breakdown:")
    for severity, count in severity_trends.items():
        logging.info(f"{severity}: {count} occurrences")

    if resolution_times:
        avg_resolution_time = sum(resolution_times) / len(resolution_times)
        logging.info(f"\nAverage Resolution Time: {avg_resolution_time:.2f} minutes")
    else:
        logging.info("\nNo resolution time data available.")

    logging.info("\nTop 5 Users with Most Errors:")
    sorted_users = sorted(user_error_count.items(), key=lambda x: x[1], reverse=True)
    for user, count in sorted_users[:5]:
        logging.info(f"User {user}: {count} errors")

def main():
    # Initialize logger
    setup_logger()

    # Read the log file
    logs = read_log_file(filename)
    if logs is None:
        return

    # Parse the logs to get trends
    error_trends, severity_trends, resolution_times, user_error_count = parse_logs(logs)

    # Calculate and log the trends
    calculate_trends(error_trends, severity_trends, resolution_times, user_error_count)

if __name__ == '__main__':
    main()

