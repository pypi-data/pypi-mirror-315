# NeuLogPy

A Python interface for NeuLog sensors, providing easy-to-use functions for data collection and experiment management.

## Features

- Simple interface for NeuLog sensors
- Real-time data collection
- Configurable sampling rates
- Support for multiple sensors
- Automatic sensor discovery and configuration
- Built-in error handling and logging

## Installation

```bash
pip install NeuLogPy
```

## Quick Start

```python
from NeuLogPy import NeuLog

# Initialize NeuLog with config file
neulog = NeuLog(config_file="config/sensors.yaml")

# Setup experiment parameters
sensor_name = "Respiration"
rate = 8        # 8 Hz sampling rate
samples = 1000  # Number of samples to collect
respiration_sensor = [(sensor_name, 1)]  # Sensor name and ID

# Start experiment
neulog.start_experiment(sensors=respiration_sensor, rate=rate, samples=samples)

# Get samples
samples = neulog.experiment.get_samples()
if samples:
    print(f"Respiration Samples: {samples}")

# Stop experiment
neulog.experiment.stop()
```

## Configuration

Create a `sensors.yaml` file in your config directory:

```yaml
sensors:
  Respiration:
    code: "RESP"
    unit: "AU"
    description: "Respiration sensor"
  # Add more sensors as needed
```

## Dependencies

- Python >= 3.7
- pydantic >= 2.0.0
- requests >= 2.25.0
- pyyaml >= 5.4.0

## Version History

- 1.2.0: Fixed package imports, improved documentation
- 1.1.1: Initial release

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Support

For support, please open an issue on the GitHub repository or contact info@sustronics.com.
