# NeuLogPy

A Python interface for NeuLog sensors, providing easy-to-use functions for data collection, experiment management, and real-time visualization.

## Features

- Simple interface for NeuLog sensors
- Real-time data collection and visualization
- Configurable sampling rates
- Support for multiple sensors
- Automatic sensor discovery and configuration
- Built-in error handling and logging
- Interactive respiratory data visualization

## Installation

```bash
pip install NeuLogPy
```

## Quick Start

### Basic Data Collection

```python
from NeuLogPy import NeuLog
import time

# Initialize NeuLog with config file
neulog = NeuLog(config_file="config/sensors.yaml")

# Setup experiment parameters
sensor_name = "Respiration"
rate = 8        # 8 Hz sampling rate
samples = 1000  # Number of samples to collect
respiration_sensor = [(sensor_name, 1)]  # Sensor name and ID

time_to_wait = samples / 8 # 8 Hz sampling rate
# Start experiment
neulog.start_experiment(sensors=respiration_sensor, rate=rate, samples=samples)
time.sleep(time_to_wait)
# Get samples
samples = neulog.experiment.get_samples()
if samples:
    print(f"Respiration Samples: {samples}")

# Stop experiment
neulog.experiment.stop()
```

### Real-time Visualization

You can use the built-in visualization tool for respiratory data:

```bash
# Run from command line
neulog-respiratory-viz
```

Or in your Python code:

```python
from NeuLogPy.respiratory_visualization import RespiratoryVisualizer

# Create and run visualizer
app = RespiratoryVisualizer()
app.setup_gui()
app.run()
```

The visualization provides:
- Real-time plotting of respiratory data
- Adjustable time window (default: 60 seconds)
- Auto-scaling axes
- Sample rate: 100 samples/second

## Configuration

Create a `sensors.yaml` file in your config directory:

```yaml
sensors:
  Respiration:
    id: 1
    name: "Respiration"
    type: "respiratory"
    units: "arbitrary"
```

## Requirements

- Python 3.7+
- NeuLog Software and Drivers
- Connected NeuLog Sensor

## Dependencies

- pydantic >= 2.0.0
- requests >= 2.25.0
- pyyaml >= 5.4.0
- dearpygui >= 1.9.0 (for visualization)

## Development

To contribute to NeuLogPy:

1. Clone the repository
```bash
git clone https://github.com/sustronics/neulogpy.git
```

2. Install development dependencies
```bash
pip install -r requirements.txt
```

3. Run tests
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact info@sustronics.com or open an issue on GitHub.
