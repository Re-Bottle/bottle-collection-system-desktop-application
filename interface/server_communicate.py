import requests

SERVER = "http://localhost:3000"  # URL of the server


def ping():
    try:
        # Sending a GET request to the server
        response = requests.get(SERVER)

        if response.status_code == 200:
            print("Ping was successful")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server")


def register_device():
    try:
        # Sending a POST request to the server
        response = requests.post(SERVER + "/device/newDevice")

        if response.status_code == 200:
            device_id = response.json()["deviceID"]
            print("Device registered with Id: ", device_id)
            return device_id
    except requests.exceptions.ConnectionError:
        print("Failed to register device")
