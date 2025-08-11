SERIAL_SETTINGS = {
    'port': 'COM3',
    'baudrate': 115200,
    'timeout': 1
}

WEATHER_THRESHOLDS = {
    'pressure': {
        'low': 1000,      #stormy/rainy weather
        'high': 1020      #clear weather
    },
    'temperature': {
        'cold': 10,       #cold
        'hot': 25         #hot
    },
    'moisture': {
        'dry': 400,       #dry soil
        'wet': 600        #wet soil
    }
}

DATA_RETENTION = {
    'max_points': 100,
    'update_interval': 1
}

FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}