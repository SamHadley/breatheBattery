from config import HISTORY_API_URL
import requests
import logging

# Function to fetch data from the API
def fetch_data(device_id):
    url = HISTORY_API_URL.format(device_id=device_id)
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Data fetched successfully from the API.")
        return response.json()
    else:
        logging.error("Failed to fetch data from the API.")
        return None


# Function to extract PM2.5 feed data from the JSON response
def extract_pm25_feed_data(data):
    pm25_levels = []
    feed_data = data.get('feeds')
    if feed_data:
        lass_dict = feed_data[0]
        if lass_dict:
            lass_list = lass_dict.get('LASS')
            for item in lass_list:
                key = list(item.keys())[0]
                value = item.get(key)
                if value:
                    pm25_d0 = value.get('s_d0')
                    pm25_d1 = value.get('s_d1')
                    timestamp = value.get('timestamp')
                    if pm25_d0 and pm25_d1 and timestamp:
                        pm25_average = (pm25_d0 + pm25_d1) / 2
                        pm25_levels.append({
                            'pm25_value': pm25_average,
                            'timestamp': timestamp
                        })
    logging.info(f"Extracted {len(pm25_levels)} PM2.5 records.")
    return pm25_levels