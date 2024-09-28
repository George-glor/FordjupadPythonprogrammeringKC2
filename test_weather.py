import unittest
import pandas as pd
from sqlalchemy import create_engine
from Weather import fetch_and_process_weather_data, insert_data_to_db

class TestWeatherData(unittest.TestCase):

    def test_data_fetching(self):
        df = fetch_and_process_weather_data()
        self.assertIsInstance(df, pd.DataFrame, "Data fetched is not a DataFrame.")
        self.assertGreater(len(df), 0, "DataFrame is empty.")
    
    def test_database_connection(self):
        try:
            engine = create_engine("mssql+pyodbc://@GEORGE/WeatherINSweden?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server")
            conn = engine.connect()
            conn.close()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_data_insertion(self):
        df = fetch_and_process_weather_data()
        try:
            insert_data_to_db(df)
        except Exception as e:
            self.fail(f"Data insertion failed: {e}")

if __name__ == '__main__':
    unittest.main()
