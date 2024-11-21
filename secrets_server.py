# secrets_server.py
import configparser
import os

CONFIG_FILE = 'config.ini'

# Default values
DEFAULTS = {
    'INFLUXDB_TOKEN': "xLQGcV7iVyNGkvtRq-2tlP5-1piy-rxBRQcavJPdgxDpW40Qc1SyPUArvKc67LaLyByab2Q7-OKlW7Es6vDdoQ==",
    'ORGANIZATION': "Pillipp_1",
    'BUCKET': "Sensors",
    'SERVER_ADDRESS': "http://172.105.78.144:8086"
}

# Load settings from the configuration file
def load_settings():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return {
            'INFLUXDB_TOKEN': config.get('Settings', 'INFLUXDB_TOKEN'),
            'ORGANIZATION': config.get('Settings', 'ORGANIZATION'),
            'BUCKET': config.get('Settings', 'BUCKET'),
            'SERVER_ADDRESS': config.get('Settings', 'SERVER_ADDRESS')
        }
    else:
        return DEFAULTS

# Save settings to the configuration file
def save_settings(token, organization, bucket, server_address):
    config = configparser.ConfigParser()
    config['Settings'] = {
        'INFLUXDB_TOKEN': token,
        'ORGANIZATION': organization,
        'BUCKET': bucket,
        'SERVER_ADDRESS': server_address
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Reset settings to default values and save them
def reset_to_defaults():
    save_settings(
        DEFAULTS['INFLUXDB_TOKEN'],
        DEFAULTS['ORGANIZATION'],
        DEFAULTS['BUCKET'],
        DEFAULTS['SERVER_ADDRESS']
    )
    print_settings()
    print("Settings have been reset to default values.")

# Function to get the current settings (instead of directly using global variables)
def get_influxdb_token():
    settings = load_settings()
    return settings['INFLUXDB_TOKEN']

def get_organization():
    settings = load_settings()
    return settings['ORGANIZATION']

def get_bucket():
    settings = load_settings()
    return settings['BUCKET']

def get_server_address():
    settings = load_settings()
    return settings['SERVER_ADDRESS']

# Print the current settings data
def print_settings():
    settings = load_settings()
    print("Current settings:")
    print(f"INFLUXDB_TOKEN: {settings['INFLUXDB_TOKEN']}")
    print(f"ORGANIZATION: {settings['ORGANIZATION']}")
    print(f"BUCKET: {settings['BUCKET']}")
    print(f"SERVER_ADDRESS: {settings['SERVER_ADDRESS']}")