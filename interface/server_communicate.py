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
