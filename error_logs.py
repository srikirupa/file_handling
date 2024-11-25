import csv
from collections import defaultdict
from datetime import datetime
import pandas as pd
import os

filename = '/usr/local/google/home/srikirupa/Downloads/error_log/error_log_data.csv'  #replace your path here

def read_log_file(filename):
    if not os.path.exists(filename):
        print(f"Error: The file {filename} was not found.")
        return None

    try:
        logs = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
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
            print(f"Warning: Missing expected field {e} in log entry.")
        except ValueError as e:
            print(f"Warning: Invalid value found in log entry: {e}")

    return error_trends, severity_trends, resolution_times, user_error_count

def calculate_trends(error_trends, severity_trends, resolution_times, user_error_count):
    """Calculates and prints trend analysis results."""

    print("\nTop 5 Error Codes:")
    sorted_error_codes = sorted(error_trends.items(), key=lambda x: x[1], reverse=True)
    for code, count in sorted_error_codes[:5]:
        print(f"{code}: {count} occurrences")


    print("\nSeverity Breakdown:")
    for severity, count in severity_trends.items():
        print(f"{severity}: {count} occurrences")


    if resolution_times:
        avg_resolution_time = sum(resolution_times) / len(resolution_times)
        print(f"\nAverage Resolution Time: {avg_resolution_time:.2f} minutes")
    else:
        print("\nNo resolution time data available.")


    print("\nTop 5 Users with Most Errors:")
    sorted_users = sorted(user_error_count.items(), key=lambda x: x[1], reverse=True)
    for user, count in sorted_users[:5]:
        print(f"User {user}: {count} errors")

def main():
    logs = read_log_file(filename)
    if logs is None:
        return  


    error_trends, severity_trends, resolution_times, user_error_count = parse_logs(logs)


    calculate_trends(error_trends, severity_trends, resolution_times, user_error_count)

if __name__ == '__main__':
    main()
