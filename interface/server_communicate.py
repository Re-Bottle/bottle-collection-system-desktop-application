import requests

SERVER = "http://localhost:8000"  # URL of the server


def ping():
    # Sending a GET request to the server
    response = requests.get(SERVER)

    if response.status_code == 200:
        print("Ping was successful")
    else:
        print(f"Failed to ping the server, response code: {response.status_code}")
