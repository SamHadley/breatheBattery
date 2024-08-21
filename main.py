import subprocess
import sys
import time
import logging
from sqlite3_db import create_db_and_table, save_data_to_db, analyze_data
from get_data import fetch_data, extract_pm25_feed_data
from config import DEVICE_ID, INTERVAL

# List of required packages
required_packages = [
    "requests",
    "pandas",
    "sqlite3"
]


# Function to install packages
def install_packages():
    for package in required_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Check if packages are installed, if not install them
def check_and_install_packages():
    try:
        import requests
        import pandas
    except ImportError:
        print("Required packages not found. Installing...")
        install_packages()


# Ensure packages are installed before running the main script
check_and_install_packages()

# Configure logging to output to both file and terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("pm25_monitor.log"),
        logging.StreamHandler()  # This will print to the terminal
    ]
)


# Function to generate a report
def generate_report(above_threshold, daily_stats):
    # Convert above_threshold DataFrame to CSV format
    above_threshold_csv = above_threshold.to_csv(index=True)

    # Convert daily_stats DataFrame to CSV format
    # Flatten MultiIndex columns for better CSV format
    daily_stats.columns = ['_'.join(col).strip() for col in daily_stats.columns.values]
    daily_stats_csv = daily_stats.to_csv(index=True)

    # Combine the two CSV sections into one report
    report = "PM2.5 Report\n"
    report += "====================\n"

    report += "\nTimes when PM2.5 was above the danger threshold:\n"
    report += above_threshold_csv

    report += "\nDaily Statistics:\n"
    report += daily_stats_csv

    # Save the report to a CSV file
    with open("pm25_report.csv", "w") as f:
        f.write(report)

    logging.info("Report generated successfully.")


if __name__ == '__main__':
    create_db_and_table()  # Ensure the database and table are created
    while True:
        json_data = fetch_data(DEVICE_ID)
        if json_data:
            pm25_levels_data = extract_pm25_feed_data(json_data)
            if pm25_levels_data:
                save_data_to_db(pm25_levels_data)
                above_threshold, daily_stats = analyze_data()
                generate_report(above_threshold, daily_stats)
        time.sleep(INTERVAL)
