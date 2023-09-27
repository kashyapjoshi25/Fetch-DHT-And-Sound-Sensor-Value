import requests
import time
import sqlite3
import os

# Specify the server's address and port
SERVER_ADDRESS = 'http://172.18.19.135:3000'

# Function to create the SQLite database and 'sensor_data' table if they don't exist
def initialize_database():
    if not os.path.isfile('dbSensor.db'):
        conn = sqlite3.connect('dbSensor.db')
        conn.close()

    conn = sqlite3.connect('dbSensor.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT,
            value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn, cursor

# Function to insert data into the database
def insert_data(conn, cursor, sensor_type, value):
    try:
        if not os.path.isfile('dbSensor.db'):
            conn, cursor = initialize_database()
        cursor.execute('''
            INSERT INTO sensor_data (sensor_type, value)
            VALUES (?, ?)
        ''', (sensor_type, value))
        conn.commit()
    except sqlite3.Error as db_error:
        print(f"SQLite Error: {db_error}")
    except Exception as other_error:
        print(f"An unexpected error occurred: {other_error}")

# Main program
try:
    conn, cursor = initialize_database()
    print("Select From Below Option")
    print("1:Temperature")
    print("2:Humidity")
    print("3.Sound")
    print("4.Fetch All Sensor Data")
    print("q:Quit")

    option = input()

    if option == 'q':
        conn.close()
        exit()

    if option in ['1', '2', '3', '4']:
        endpoint = 'temperature' if option == '1' else ('humidity' if option == '2' else ('sound' if option == '3' else 'fetch_all'))

        while True:
            response = requests.get(f'{SERVER_ADDRESS}/{endpoint}')

            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"Error: {data['error']}")
                else:
                    if endpoint != 'fetch_all':
                        if endpoint in data:
                            value = data[endpoint]
                            print(f"{endpoint.capitalize()}: {value:.2f}")
                            insert_data(conn, cursor, endpoint, value)
                            print(f"Data inserted into database: {endpoint}: {value}")
                    else:
                        for sensor_type, value in data.items():
                            print(f"{sensor_type.capitalize()}: {value}")
                            insert_data(conn, cursor, sensor_type, value)
                            print(f"Data inserted into database: {sensor_type}: {value}")

            else:
                print(f"Failed to retrieve {endpoint} data. Status code: {response.status_code}")
				
            time.sleep(2)  # Wait for 2 seconds before making the next request

except requests.exceptions.RequestException as request_error:
    print(f"Request Error: {request_error}")
except Exception as other_error:
    print(f"An unexpected error occurred: {other_error}")
finally:
    conn.close()
