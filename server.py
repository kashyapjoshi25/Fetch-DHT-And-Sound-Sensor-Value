from flask import Flask, jsonify
import Adafruit_DHT
import RPi.GPIO as GPIO

app = Flask(__name__)

# Define the GPIO pins where your DHT sensor and sound sensor are connected.
DHT_SENSOR_PIN = 4  # GPIO 4 (BCM numbering)
SOUND_SENSOR_PIN = 26  # GPIO 26 (BCM numbering)

# Configure the GPIO mode
GPIO.setmode(GPIO.BCM)

@app.route('/temperature', methods=['GET'])
def get_temperature():
    try:
        # Read data from the DHT sensor
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, DHT_SENSOR_PIN)

        if temperature is not None:
            # If the sensor reading is successful, return temperature as JSON
            return jsonify({'temperature': temperature})
        else:
            # If the sensor reading fails, return an error response as JSON
            return jsonify({'error': 'Failed to retrieve temperature data'}), 500
    except Exception as e:
        # Handle any exceptions that may occur during sensor reading
        return jsonify({'error': str(e)}), 500

@app.route('/humidity', methods=['GET'])
def get_humidity():
    try:
        # Read data from the DHT sensor
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, DHT_SENSOR_PIN)

        if humidity is not None:
            # If the sensor reading is successful, return humidity as JSON
            return jsonify({'humidity': humidity})
        else:
            # If the sensor reading fails, return an error response as JSON
            return jsonify({'error': 'Failed to retrieve humidity data'}), 500
    except Exception as e:
        # Handle any exceptions that may occur during sensor reading
        return jsonify({'error': str(e)}), 500

@app.route('/sound', methods=['GET'])
def get_sound():
    try:
        GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)
        sound_level = GPIO.input(SOUND_SENSOR_PIN)
        # Return the sound data as JSON
        return jsonify({'sound_level': sound_level})
    except Exception as e:
        # Handle any exceptions that may occur during sound sensor reading
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_all', methods=['GET'])
def fetch_all_data():
    try:
        # Read data from the DHT sensor for temperature and humidity
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, DHT_SENSOR_PIN)

        # Read data from the sound sensor
        GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)
        sound_level = GPIO.input(SOUND_SENSOR_PIN)

        data = {
            'temperature': temperature,
            'humidity': humidity,
            'sound_level': sound_level
        }

        return jsonify(data)
    except Exception as e:
        # Handle any exceptions that may occur during sensor reading
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='172.18.19.135', port=3000)
