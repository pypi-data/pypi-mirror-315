import requests
import json
from .logger import setup_logger

class NeuLogAPIClient:
    def __init__(self, host='localhost', port=22004):
        """Initialize API client
        
        Args:
            host (str): NeuLog server host
            port (int): NeuLog server port
        """
        self.logger = setup_logger(__name__)
        self.base_url = f"http://{host}:{port}/NeuLogAPI"
        self.logger.info(f"Initializing NeuLog API client at {self.base_url}")
        
    def send_request(self, command, params=""):
        """Send request to NeuLog API
        
        Args:
            command (str): API command
            params (str): Command parameters
            
        Returns:
            dict: Response from NeuLog server
        """
        url = f"{self.base_url}?{command}:{params}"
        self.logger.debug(f"Sending request to: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse response
            raw_response = response.text
            self.logger.debug(f"Raw response: {raw_response}")
            
            try:
                return json.loads(raw_response)
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse response as JSON: {raw_response}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None
