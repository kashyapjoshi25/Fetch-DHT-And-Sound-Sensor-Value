# Fetch-DHT-And-Sound-Sensor-Value
Fetching the DHT(Humidity And Temperature) And Sound sensor value. Sensors are hosted on Rasberry Pi

#### API Endpoints and Their Functionality:

**1) `/temperature` (GET):**  
This API endpoint retrieves real-time temperature data from a DHT11 temperature and humidity sensor connected to the Raspberry Pi. The data is returned in JSON format, encapsulated within the key "temperature."

**2) `/humidity` (GET):**  
The `/humidity` endpoint serves to obtain current humidity data from the same DHT11 sensor. Similar to temperature, the data is provided in JSON format, labeled under the key "humidity."

**3) `/sound` (GET):**  
The `/sound` API endpoint is responsible for fetching the present sound level recorded by a sound sensor attached to the Raspberry Pi. The result is conveyed as an integer, representing the sound level.

**4) `/fetch-all` (GET):**  
The `/fetch-all` endpoint combines the functionalities of `/temperature`, `/humidity`, and `/sound`. It consolidates these sensor readings into a single JSON object, encompassing keys such as "temperature," "humidity," and "sound."

#### Client Script Functionality:

The client script, `client.py`, serves as an interface for users to interact with the Raspberry Pi-based server. Here's a step-by-step explanation of its operation:

1. **Initialization:** The script initiates a connection to the Raspberry Pi server, identified by the address `172.18.19.135` and port `3000`.

2. **User Menu:** Users are presented with a menu that offers various options:
   - "1": Retrieve and display current temperature data.
   - "2": Fetch and display current humidity data.
   - "3": Acquire and display current sound level data.
   - "4": Fetch all sensor data (temperature, humidity, and sound) in a single request.
   - "q": Quit the program.

3. **Option Selection:** Depending on the chosen option, the script sends an HTTP GET request to the corresponding API endpoint on the Raspberry Pi server.

4. **Response Handling:** The client script processes the server's response as follows:
   - For sensor data (temperature, humidity, or sound), the script displays the data on the console and inserts it into a local SQLite database.
   - In the event of an error or an invalid option, an error message is presented.

5. **Repeat Action:** The script waits for 2 seconds before repeating the chosen action (excluding "q") in a loop, ensuring periodic data updates.

#### Local Database Schema:

The local SQLite database, named `dbSensor.db`, features a single table known as `sensor_data`. This table possesses the following columns:

- `id` (INTEGER, PRIMARY KEY AUTOINCREMENT): An auto-incremented unique identifier for each record.
- `sensor_type` (TEXT): Indicates the type of sensor data (e.g., "temperature," "humidity," "sound").
- `value` (REAL): Stores the recorded sensor reading value.
- `timestamp` (DATETIME, DEFAULT CURRENT_TIMESTAMP): Captures the timestamp of data insertion, defaulting to the current timestamp.

This schema enables the storage and retrieval of sensor data for further analysis and utilization.
