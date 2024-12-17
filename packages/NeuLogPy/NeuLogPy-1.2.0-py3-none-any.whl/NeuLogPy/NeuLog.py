# neu_log.py

from NeuLogPy.core.api_client import NeuLogAPIClient
from NeuLogPy.core.sensor_registry import SensorRegistry
from NeuLogPy.core.experiment import Experiment

class NeuLog:
    def __init__(self, config_file="config/sensors.yaml", host='localhost', port=22004):
        """Initialize NeuLog interface.
        
        Args:
            config_file (str): Path to sensors.yaml config file
            host (str): NeuLog server host (default: localhost)
            port (int): NeuLog server port (default: 22004)
        """
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


# Usage Example in neu_log.py

if __name__ == "__main__":
    registry = SensorRegistry(config_file="config/sensors.yaml")
    
    # List all sensors from the YAML file
    print("Initial Sensors:")
    registry.list_sensors()
    
    # Add a new sensor
    registry.add_sensor(name="CO2", code="CO2", unit="ppm", description="Measures carbon dioxide levels")
    
    # List all sensors again, including the new one
    print("\nSensors after adding CO2:")
    registry.list_sensors()
