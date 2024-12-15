import requests
import jwt
import json

class NixteeClient:
    def __init__(self, api_url="https://api.nixtee.com"):
        self.api_url = api_url
        self.token = None

    def authorize(self, email, password):
        url = f"{self.api_url}/auth/login"
        data = {"email": email, "password": password}
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            self.token = response.json().get("token")
            if not self.token:
                raise Exception("Authorization token not found in response.")
            return self.token
        else:
            raise Exception(f"Authorization failed: {response.json().get('message', response.text)}")

    def train(self, model_data):
        return self._authorized_request("POST", "/train", model_data)

    def save(self, model_id, data):
        return self._authorized_request("POST", f"/models/{model_id}/save", data)

    def load(self, model_id):
        return self._authorized_request("GET", f"/models/{model_id}/load")

    def predict(self, model_id, input_data):
        return self._authorized_request("POST", f"/models/{model_id}/predict", input_data)

    def classify(self, model_id, input_data):
        return self._authorized_request("POST", f"/models/{model_id}/classify", input_data)

    def _authorized_request(self, method, endpoint, data=None):
        if not self.token:
            raise Exception("Authorization token is missing. Please login first.")
        
        url = f"{self.api_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        
        response = requests.request(method, url, headers=headers, json=data)
        
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.json().get('message', response.text)}")

