import dearpygui.dearpygui as dpg
from NeuLogPy.NeuLog import NeuLog
from NeuLogPy.core.logger import setup_logger
import time
from collections import deque
import signal
import sys

class RespiratoryVisualizer:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.neulog = NeuLog()
        self.recording = False
        self.data = deque(maxlen=10000)  # Store last 10000 samples
        self.sample_rate = 100  # 100 samples per second
        self.window_size = 60.0  # 60 second window
        self.start_time = 0

    def setup_gui(self):
        dpg.create_context()

        # Create window
        with dpg.window(label="Respiratory Data Monitor", tag="primary_window"):
            # Status and controls
            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text("Ready", tag="status_text", color=(0, 255, 0))

            dpg.add_separator()

            # Window size control
            with dpg.group(horizontal=True):
                dpg.add_text("Window Size (seconds):")
                dpg.add_input_float(
                    default_value=60.0,
                    format="%.1f",
                    callback=lambda s, a: self.update_window_size(a),
                    width=100,
                    tag="window_size"
                )

            # Plot
            with dpg.plot(label="Respiratory Data", height=400, width=-1, tag="resp_plot"):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="x_axis")
                with dpg.plot_axis(dpg.mvYAxis, label="Respiratory Value", tag="y_axis"):
                    # Create series with enough points for the window
                    dpg.add_line_series(
                        [i/self.sample_rate for i in range(int(self.window_size * self.sample_rate))],
                        [0] * int(self.window_size * self.sample_rate),
                        label="Respiratory Data",
                        tag="resp_data"
                    )

        dpg.create_viewport(title="Respiratory Data Monitor", width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("primary_window", True)

    def update_window_size(self, new_size: float):
        self.window_size = max(1.0, new_size)
        # Update x-axis series
        dpg.configure_item("resp_data", x=[i/self.sample_rate for i in range(int(self.window_size * self.sample_rate))])

    def update_plot(self):
        if not self.data:
            return

        # Calculate how many samples we need for the window
        samples_needed = int(self.window_size * self.sample_rate)
        
        # Get the last N samples that fit in our window
        data_list = list(self.data)
        if len(data_list) > samples_needed:
            visible_values = data_list[-samples_needed:]
        else:
            # If we have fewer samples than needed, pad with zeros at the start
            visible_values = [0] * (samples_needed - len(data_list)) + data_list

        # Create x values based on sample rate
        x_values = [i/self.sample_rate for i in range(len(visible_values))]

        # Set axis limits
        dpg.set_axis_limits("x_axis", 0, self.window_size)
        if visible_values:
            min_val = min(visible_values)
            max_val = max(visible_values)
            range_val = max_val - min_val if max_val != min_val else 1.0
            dpg.set_axis_limits("y_axis", 
                              min_val - range_val * 0.1,
                              max_val + range_val * 0.1)
            dpg.set_value("resp_data", [x_values, visible_values])

    def start_experiment(self):
        # Define experiment parameters
        SENSOR_NAME = "Respiration"
        SENSOR_ID = 1
        RATE = 5  # 100 samples per second
        SAMPLES = 10000  # Large number for continuous streaming
        
        self.logger.info(f"\nStarting {SENSOR_NAME} sensor streaming...")
        self.logger.info(f"Rate: {RATE} (100 samples/sec)")
        
        # Try to connect to NeuLog server
        try:
            # Test connection first
            test_response = self.neulog.api_client.send_request("GetServerVersion")
            if test_response is None:
                self.logger.error("""
NeuLog server not found at http://localhost:22004
Please ensure that:
1. NeuLog software is installed on your computer
2. NeuLog software is running
3. NeuLog device is connected to your computer
""")
                return False
                
            # Start the experiment
            response = self.neulog.start_experiment([(SENSOR_NAME, SENSOR_ID)], RATE, SAMPLES)
            if not response or not response.get("StartExperiment", False):
                self.logger.error("Failed to start experiment. Check if the sensor is properly connected.")
                return False
                
            self.logger.info("Experiment started successfully")
            self.start_time = time.time()
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting experiment: {e}")
            return False

    def run(self):
        if not self.start_experiment():
            return

        prev_len = 2
        try:
            while dpg.is_dearpygui_running():
                # Get latest samples
                response = self.neulog.experiment.get_samples()
                
                if response and isinstance(response, dict):
                    samples = response.get("GetExperimentSamples", [])
                    if isinstance(samples, list) and len(samples) > 0:
                        # Process each sample data
                        for sample_data in samples:
                            if len(sample_data) >= 3 and sample_data[0] == "Respiration":
                                values = sample_data[prev_len:]
                                # Add each value to our deque
                                for value in values:
                                    try:
                                        self.data.append(float(value))
                                    except (ValueError, TypeError):
                                        continue
                                prev_len = len(sample_data)-1
                        
                        if self.data:  # Only update plot if we have data
                            self.update_plot()
                
                dpg.render_dearpygui_frame()
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
        except Exception as e:
            self.logger.error(f"Error during experiment: {e}")
            raise  # Re-raise to see the full error
        finally:
            # Clean up
            self.logger.info("\nStopping experiment...")
            self.neulog.experiment.stop()
            self.logger.info("Experiment stopped.")
            dpg.destroy_context()

def main():
    app = RespiratoryVisualizer()
    app.setup_gui()
    app.run()

if __name__ == "__main__":
    main()
