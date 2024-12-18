# neu_log.py

import time
import yaml
from .core.api_client import NeuLogAPIClient
from .core.sensor_registry import SensorRegistry
from .core.experiment import Experiment
from .core.logger import setup_logger

class NeuLog:
    def __init__(self, config_file="config/sensors.yaml", host='localhost', port=22004):
        """Initialize NeuLog interface.
        
        Args:
            config_file (str): Path to sensor configuration file
            host (str): NeuLog server host (default: localhost)
            port (int): NeuLog server port (default: 22004)
        """
        self.logger = setup_logger(__name__)
        
        # Load configuration
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
            config = {}
        
        # Initialize components
        host = config.get('host', host)
        port = config.get('port', port)
        
        self.api_client = NeuLogAPIClient(host, port)
        self.sensor_registry = SensorRegistry(config_file)
        self.experiment = None

    def start_experiment(self, sensors, rate, samples):
        """Start a new experiment.
        
        Args:
            sensors (list): List of (sensor_name, sensor_id) tuples
            rate (int): Sampling rate index
            samples (int): Number of samples to collect
            
        Returns:
            dict: Response from NeuLog server
        """
        sensor_data = [(self.sensor_registry.get_sensor(name),id) for name, id in sensors]
        self.experiment = Experiment(self.api_client, sensor_data, rate, samples)
        return self.experiment.start()

    def list_sensors(self):
        """List all available sensors from config."""
        self.sensor_registry.list_sensors()

    def get_sensor_value(self, sensor_code, sensor_id):
        """Get real-time value from a sensor.
        
        Args:
            sensor_code (str): The sensor code (e.g., 'Respiration')
            sensor_id (int): The sensor ID
            
        Returns:
            float: Current sensor value
        """
        return self.experiment.get_sensor_value(sensor_code, sensor_id)


# Usage Example in neu_log.py

if __name__ == "__main__":
    registry = SensorRegistry("config/sensors.yaml")

    neulog = NeuLog(config_file="config/sensors.yaml")
    
    # Start an experiment
    neulog.start_experiment([("Respiration", 1)], 5, 1000)
    time.sleep(10)
    neulog.logger.info(neulog.experiment.get_samples()) 
    neulog.experiment.stop()
    
    # List all sensors from the YAML file
    neulog.logger.info("Initial Sensors:")
    registry.list_sensors()
    
    # Add a new sensor
    registry.add_sensor(name="CO2", code="CO2", unit="ppm", description="Measures carbon dioxide levels")
    
    # List all sensors again, including the new one
    neulog.logger.info("\nSensors after adding CO2:")
    registry.list_sensors()
