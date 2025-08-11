from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import serial
import threading
import time
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dewdrop'
socketio = SocketIO(app, cors_allowed_origins="*")

sensor_data = {
    'temperature': deque(maxlen=100),
    'pressure': deque(maxlen=100),
    'moisture': deque(maxlen=100),
    'timestamps': deque(maxlen=100),
    'rssi': deque(maxlen=100),
    'snr': deque(maxlen=100)
}

current_weather = {
    'temperature': 0,
    'pressure': 0,
    'moisture': 0,
    'rssi': 0,
    'snr': 0,
    'timestamp': datetime.now(),
    'weather_condition': 'Unknown',
    'forecast': []
}

serial_port = None
serial_thread = None
is_running = False

def connect_serial():
    global serial_port
    ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8']
    
    for port in ports:
        try:
            serial_port = serial.Serial(port, 115200, timeout=1)
            print(f"Connected to {port}")
            return True
        except:
            continue
    
    print("No serial connection found - using simulated data")
    return False

def parse_sensor_data(line):
    try:
        parts = line.strip().split(',')
        if len(parts) >= 6:
            millis = int(parts[0])
            temp = float(parts[1])
            pres = float(parts[2])
            moist = int(parts[3])
            rssi = int(parts[4])
            snr = float(parts[5])
            
            return {
                'temperature': temp,
                'pressure': pres,
                'moisture': moist,
                'rssi': rssi,
                'snr': snr,
                'timestamp': datetime.now()
            }
    except:
        pass
    return None

def simulate_sensor_data():
    base_temp = 20 + 5 * math.sin(time.time() / 100)
    base_pressure = 1013 + 10 * math.sin(time.time() / 200)
    base_moisture = 500 + 100 * math.sin(time.time() / 150)
    
    return {
        'temperature': base_temp + np.random.normal(0, 0.5),
        'pressure': base_pressure + np.random.normal(0, 2),
        'moisture': int(base_moisture + np.random.normal(0, 10)),
        'rssi': -60 + np.random.randint(-10, 10),
        'snr': 8 + np.random.normal(0, 1),
        'timestamp': datetime.now()
    }

def determine_weather_condition(temp, pressure, moisture):
    if pressure < 1000:
        if temp > 25:
            return "Stormy"
        else:
            return "Rainy"
    elif pressure > 1020:
        if temp > 25:
            return "Hot and Clear"
        else:
            return "Clear"
    else:
        if moisture > 600:
            return "Humid"
        elif temp < 10:
            return "Cold"
        else:
            return "Partly Cloudy"

def generate_forecast(current_data):
    forecast = []
    
    if len(sensor_data['temperature']) > 5:
        temp_trend = np.mean(list(sensor_data['temperature'])[-5:]) - np.mean(list(sensor_data['temperature'])[-10:-5]) if len(sensor_data['temperature']) >= 10 else 0
        pressure_trend = np.mean(list(sensor_data['pressure'])[-5:]) - np.mean(list(sensor_data['pressure'])[-10:-5]) if len(sensor_data['pressure']) >= 10 else 0
    else:
        temp_trend = 0
        pressure_trend = 0
    
    for i in range(1, 7):
        future_time = datetime.now() + timedelta(hours=i)
        
        future_temp = current_data['temperature'] + (temp_trend * i * 0.5)
        future_pressure = current_data['pressure'] + (pressure_trend * i * 0.3)
    
        
        condition = determine_weather_condition(future_temp, future_pressure, current_data['moisture'])
        
        forecast.append({
            'time': future_time.strftime('%H:%M'),
            'temperature': round(future_temp, 1),
            'pressure': round(future_pressure, 1),
            'condition': condition
        })
    
    return forecast

def sensor_reader():
    global current_weather, is_running
    
    while is_running:
        try:
            if serial_port and serial_port.is_open:
                line = serial_port.readline().decode('utf-8').strip()
                if line and not line.startswith('millis'):
                    data = parse_sensor_data(line)
                    if data:
                        update_sensor_data(data)
            else:
                data = simulate_sensor_data()
                update_sensor_data(data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            time.sleep(5)

def update_sensor_data(data):
    global current_weather
    
    sensor_data['temperature'].append(data['temperature'])
    sensor_data['pressure'].append(data['pressure'])
    sensor_data['moisture'].append(data['moisture'])
    sensor_data['rssi'].append(data['rssi'])
    sensor_data['snr'].append(data['snr'])
    sensor_data['timestamps'].append(data['timestamp'])
    
    current_weather.update(data)
    current_weather['weather_condition'] = determine_weather_condition(
        data['temperature'], data['pressure'], data['moisture']
    )
    current_weather['forecast'] = generate_forecast(data)
    
    current_serializable = current_weather.copy()
    current_serializable['timestamp'] = current_weather['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    socketio.emit('sensor_update', {
        'current': current_serializable,
        'historical': {
            'temperature': list(sensor_data['temperature']),
            'pressure': list(sensor_data['pressure']),
            'moisture': list(sensor_data['moisture']),
            'timestamps': [t.strftime('%H:%M:%S') for t in sensor_data['timestamps']]
        }
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current')
def api_current():
    current_serializable = current_weather.copy()
    current_serializable['timestamp'] = current_weather['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(current_serializable)

@app.route('/api/historical')
def api_historical():
    return jsonify({
        'temperature': list(sensor_data['temperature']),
        'pressure': list(sensor_data['pressure']),
        'moisture': list(sensor_data['moisture']),
        'timestamps': [t.strftime('%H:%M:%S') for t in sensor_data['timestamps']]
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    current_serializable = current_weather.copy()
    current_serializable['timestamp'] = current_weather['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    emit('sensor_update', {
        'current': current_serializable,
        'historical': {
            'temperature': list(sensor_data['temperature']),
            'pressure': list(sensor_data['pressure']),
            'moisture': list(sensor_data['moisture']),
            'timestamps': [t.strftime('%H:%M:%S') for t in sensor_data['timestamps']]
        }
    })

if __name__ == '__main__':
    try:
        connect_serial()
        
        is_running = True
        serial_thread = threading.Thread(target=sensor_reader, daemon=True)
        serial_thread.start()
        
        print("Starting DewDrop Weather Station...")
        
        app_started = False
        
        print(f"Open http://localhost:5000 in your browser")
        socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        app_started = True

    except KeyboardInterrupt:
        is_running = False
        if serial_port:
            serial_port.close()
        print("\nShutting down DewDrop Weather Station...")
    
    if not app_started:
        print("Could not start the application on any available port.")
        is_running = False
        if serial_port:
            serial_port.close()