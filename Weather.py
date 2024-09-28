
import pyodbc
import requests
import pandas as pd
from sqlalchemy import create_engine
import logging

# Set up logging
logging.basicConfig(filename='historical_weather_task.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_process_weather_data():
    """Fetches and processes weather data from the API."""
    # Parameters for the API request
    latitude = 59.33  
    longitude = 18.07  
    start_date = "2021-01-01"
    end_date = "2021-12-31"
    url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        
        # Convert data to DataFrame
        hourly_data = data['hourly']
        df = pd.DataFrame(hourly_data)

        df['time'] = pd.to_datetime(df['time'])

        if df.isnull().values.any():
            logging.warning("Data contains missing values. Filling with default values.")
            df.fillna({'temperature_2m': 0, 'relative_humidity_2m': 50, 'wind_speed_10m': 0}, inplace=True)

        df['temperature_2m'] = df['temperature_2m'] * 9/5 + 32

        logging.info(f"Transformed DataFrame Columns and Types:\n{df.dtypes}")
        logging.info(f"Sample Transformed Data:\n{df.head()}")

        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the API request: {e}")
        raise e

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise e

def insert_data_to_db(df):
    """Inserts the DataFrame into the database."""
    try:
        engine = create_engine("mssql+pyodbc://@GEORGE/WeatherINSweden?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server")
        df.to_sql('weather_forecast', con=engine, if_exists='append', index=False)
        logging.info("Historical weather data inserted successfully.")
        print("Data inserted successfully.")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        raise e

if __name__ == '__main__':
    df = fetch_and_process_weather_data()
    insert_data_to_db(df)
