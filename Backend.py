import os
import time
import random
import threading
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# Simulated sensor reading functions (replace with actual sensor libraries)
def read_dht22():
    """Simulate DHT22 temperature and humidity reading"""
    return {
        'temperature': round(random.uniform(20.0, 30.0), 1),
        'humidity': round(random.uniform(40.0, 60.0), 1)
    }

def read_mq135():
    """Simulate MQ135 air quality reading"""
    return {
        'co2_equivalent': round(random.uniform(400, 1000), 1),
        'tvoc': round(random.uniform(0, 500), 1)
    }

def read_sound_sensor():
    """Simulate sound level reading"""
    return {
        'decibel_level': round(random.uniform(30.0, 80.0), 1)
    }

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variable to store latest sensor readings
sensor_data = {
    'temperature': 0,
    'humidity': 0,
    'co2_equivalent': 0,
    'tvoc': 0,
    'decibel_level': 0
}

def update_sensor_readings():
    """Continuously update sensor readings"""
    global sensor_data
    while True:
        # Read from simulated sensors
        dht_data = read_dht22()
        mq_data = read_mq135()
        sound_data = read_sound_sensor()

        # Update global sensor data
        sensor_data.update({
            'temperature': dht_data['temperature'],
            'humidity': dht_data['humidity'],
            'co2_equivalent': mq_data['co2_equivalent'],
            'tvoc': mq_data['tvoc'],
            'decibel_level': sound_data['decibel_level']
        })

        # Emit sensor data via WebSocket
        socketio.emit('sensor_update', sensor_data)
        
        # Wait before next reading
        time.sleep(5)

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/api/sensor_data')
def get_sensor_data():
    """API endpoint to retrieve current sensor data"""
    return jsonify(sensor_data)

if __name__ == '__main__':
    # Start sensor reading thread
    sensor_thread = threading.Thread(target=update_sensor_readings)
    sensor_thread.daemon = True
    sensor_thread.start()

    # Run Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)