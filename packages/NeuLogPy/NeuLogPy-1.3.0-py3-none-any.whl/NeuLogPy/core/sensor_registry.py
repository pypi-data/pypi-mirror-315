# core/sensor_registry.py

from .logger import setup_logger
from ..models.sensor import Sensor, SensorConfig
from ..utils.file_loader import load_yaml

class SensorRegistry:
    def __init__(self, config_file="config/sensors.yaml"):
        """Initialize sensor registry.
        
        Args:
            config_file (str): Path to sensor configuration file
        """
        self.logger = setup_logger(__name__)
        raw_data = load_yaml(config_file)
        self.sensor_config = SensorConfig(**raw_data)  # Validate and load the sensor config

    def get_sensor(self, name):
        """Retrieve a sensor by name.
        
        Args:
            name (str): Name of the sensor
            
        Returns:
            Sensor: Sensor object if found, None otherwise
        """
        sensor = self.sensor_config.sensors.get(name)
        if not sensor:
            self.logger.warning(f"Sensor {name} not found")
            return None
        return sensor
    
    def add_sensor(self, name, code, unit="", description=""):
        """Add a new sensor and validate it using the Sensor Pydantic model.
        
        Args:
            name (str): Name of the sensor
            code (str): Sensor code
            unit (str, optional): Unit of measurement
            description (str, optional): Sensor description
        """
        if name in self.sensor_config.sensors:
            self.logger.warning(f"Sensor {name} already exists, updating...")
        
        self.sensor_config.sensors[name] = Sensor(code=code, unit=unit, description=description)
        self.logger.info(f"Added sensor: {name} (code: {code})")
    
    def list_sensors(self):
        """List all sensors with their details."""
        if not self.sensor_config.sensors:
            self.logger.info("No sensors registered")
            return
        
        for name, details in self.sensor_config.sensors.items():
            self.logger.info(f"{name}: {details.code} - {details.description}")
    
    def remove_sensor(self, name):
        """Remove a sensor from the registry.
        
        Args:
            name (str): Name of the sensor
            
        Returns:
            bool: True if sensor is removed, False otherwise
        """
        if name not in self.sensor_config.sensors:
            self.logger.warning(f"Sensor {name} not found")
            return False
        
        del self.sensor_config.sensors[name]
        self.logger.info(f"Removed sensor: {name}")
        return True
