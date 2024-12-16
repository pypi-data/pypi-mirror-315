import os
from typing import List, Dict, Any, Union
import requests
import json

class Router:
    """
    A class to interact with the Mintii API for routing LLM requests.
    """

    def __init__(self, api_key: str = None, router_name: str = "custom-default"):
        """
        Initializes the Router with an API key.

        Args:
            api_key (str, optional): The Mintii API key.
                If not provided, it will attempt to read from the MINTII_API_KEY environment variable.
             router_name (str, optional): The name of the router to use. Defaults to "custom-default".
        Raises:
            ValueError: If no API key is provided and the MINTII_API_KEY environment variable is not set.
        """
        self.api_key = api_key or os.getenv("MINTII_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided and MINTII_API_KEY environment variable not set."
            )
        self.router_name = router_name
        self.api_url = "https://api.mintii.ai/route/custom/v1"

    def generate(self, prompt: Union[str, List[Dict[str, str]]]) -> Dict[str, Any]:
         """
        Routes a prompt to the Mintii API.

        Args:
            prompt (str | List[Dict[str, str]]): The prompt to send to the API.
                It can be a single string or a list of messages as a dictionary
                with keys "role" and "content". If a string is passed, it's
                converted into a user message. If a list of messages is passed,
                it's used directly.
        Returns:
            Dict[str, Any]: The JSON response from the API.
        Raises:
             requests.exceptions.RequestException: If the API request fails.
        """
         if isinstance(prompt, str):
            prompt = [{"role": "user", "content": prompt}]

         headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
         }
         payload = {"prompt": prompt}
         params = {"router_name": self.router_name}

         try:
            response = requests.post(
                self.api_url,
                headers=headers,
                params=params,
                data=json.dumps(payload),
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
         except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            raise