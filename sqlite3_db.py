import pandas as pd
import sqlite3
import logging
from config import THRESHOLD


# Function to create the SQLite database and table if it doesn't exist
def create_db_and_table():
    conn = sqlite3.connect('pm25_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pm25_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pm25_value REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Database and table created (if not already present).")


# Function to save data to SQLite database, avoiding duplicates
def save_data_to_db(data):
    conn = sqlite3.connect('pm25_data.db')
    df = pd.DataFrame(data)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Load existing data to check for duplicates
    existing_df = pd.read_sql_query("SELECT * FROM pm25_history", conn)
    existing_df['timestamp'] = pd.to_datetime(existing_df['timestamp'])

    # Append only new records
    new_data = df[~df['timestamp'].isin(existing_df['timestamp'])]
    if not new_data.empty:
        new_data.to_sql('pm25_history', conn, if_exists='append', index=False)
        logging.info(f"Saved {len(new_data)} new records to the database.")
        logging.info(f"Database currently has {len(existing_df)} PM2.5 records.")
    else:
        logging.info("No new data to save.")
        logging.info(f"Database currently has {len(existing_df)} PM2.5 records.")

    conn.close()


# Function to analyze the data
def analyze_data():
    conn = sqlite3.connect('pm25_data.db')
    df = pd.read_sql_query("SELECT * FROM pm25_history", conn)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Filter data where PM2.5 is above the threshold
    above_threshold = df[df['pm25_value'] > THRESHOLD]

    # Daily statistics
    daily_stats = df.resample('D').agg({
        'pm25_value': ['max', 'min', 'mean']
    })

    conn.close()
    logging.info("Data analysis completed.")
    return above_threshold, daily_stats