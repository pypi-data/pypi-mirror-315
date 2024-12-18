from .logger import setup_logger

class Experiment:
    def __init__(self, api_client, sensors, rate, samples):
        self.api_client = api_client
        self.sensors = sensors
        self.rate = rate
        self.samples = samples
        self.logger = setup_logger(__name__)

    def start(self):
        """Start a new experiment"""
        sensor_params = ",".join([f"[{sensor.code}],[{id}]" for sensor,id in self.sensors])
        response = self.api_client.send_request("StartExperiment", f"{sensor_params},[{self.rate}],[{self.samples}]")
        if response and response.get("StartExperiment") == "True":
            return {"StartExperiment": True}
        return None

    def stop(self):
        """Stop the current experiment"""
        response = self.api_client.send_request("StopExperiment")
        if response and response.get("StopExperiment") == "True":
            return {"StopExperiment": True}
        return None

    def get_samples(self):
        """Get samples from the current experiment"""
        sensor_params = ",".join([f"[{sensor.code}],[{id}]" for sensor,id in self.sensors])
        return self.api_client.send_request("GetExperimentSamples", sensor_params)
