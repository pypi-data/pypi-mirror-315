import requests
BASE_URL  = "https://api-development.roojh.com/api/v1"

class DeviceAPI:
    def __init__(self, client_id: str = "roojh-beta-anuj"):
        self.client_id = client_id
        self.api_url = f"{BASE_URL}/devices/"
    
    def get_devices(self):
        """
        Fetch devices from the API and return the response.
        """
        try:
            response = requests.get(f"{self.api_url}getDevicesByClientId?clientId={self.client_id}")
            response.raise_for_status()  # Raise an error for bad HTTP status
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return None

    def filter_devices(self, devices, status_filter=None):
        """
        Filter devices based on status (active/inactive).
        """
        if status_filter:
            return [device for device in devices if device['status'] == status_filter]
        return devices
    
    def get_device(self, device_id):
        """
        Get detailed information about a specific device.
        """
        try:
            response = requests.get(f"{self.api_url}getDeviceById?clientId={self.client_id}&deviceId={device_id}")
            response.raise_for_status()  # Raise an error for bad HTTP status
            return response.json()
        except requests.exceptions.RequestException:
            print(f"\nSomething went wrong!")            
            return None
        
    def updateComponentOnDevice(self, deviceId, portPath, recipeName, mode):
        """
        Update a component on a device.
        """
        try:
            headers = { "Content-Type": "application/json"}
            payload = {
                "clientId": self.client_id,
                "deviceId": deviceId,
                "componentInput": {
                    "rvCaptureStreamingComponentUnifiedInput": {
                        "mode" : mode,
                        "recipeName": recipeName,
                        "portPath": portPath
                    }
                }
            }
            response = requests.post(f"{self.api_url}updateUnifiedComponentsOnDevice", headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad HTTP status
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating component on device {e}")
            return None
        
    def assignDeviceToBed(self, deviceId, bedId, hospitalId):
        """
        Assign a device to a bed.
        """
        try:
            headers = { "Content-Type": "application/json"}
            payload = {
                "clientId": self.client_id,
                "deviceId": deviceId,
                "bedId": bedId,
                "hospitalId": hospitalId
            }
            response = requests.post(f"{self.api_url}assignDeviceToBed", headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad HTTP status
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"\nError assigning device to bed {e}")
            return None

    def getDevicesInfo(self, deviceIds):
        """
        Get detailed information about multiple devices.
        """
        try:
            headers = { "Content-Type": "application/json"}
            payload = {
                "deviceIds": deviceIds
            }
            response = requests.post(f"{self.api_url}getDeviceInfoByIds", headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad HTTP status
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"\nError getting devices info {e}")
            return None