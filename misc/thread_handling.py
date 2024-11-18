import threading
from utility import connect_wifi


def connect_to_wifi(callback_function, SSID, password):
    """
    Connect to a Wi-Fi network based on the current operating system.

    :param callback_function: The function to call after the connection attempt.
    :param SSID: The Wi-Fi network name (SSID).
    :param password: The Wi-Fi network password.
    """

    # This function will be run in a separate thread to avoid blocking the main thread
    def wifi_connection_thread():
        try:
            # Attempt to connect to Wi-Fi
            connect_wifi(SSID, password)
            # After successful connection, call the callback function
            callback_function(True)  # Pass True if successful
        except Exception as e:
            # If there was an error during connection, call the callback with False
            print(f"Error connecting to Wi-Fi: {e}")
            callback_function(False)  # Pass False if there was an error

    # Create a thread to run the connection process in the background
    thread = threading.Thread(target=wifi_connection_thread)
    thread.start()


# Example callback function to handle the result of the Wi-Fi connection attempt
def connection_callback(success):
    if success:
        print("Successfully connected to Wi-Fi!")
    else:
        print("Failed to connect to Wi-Fi.")


# Example for connecting to a new WIFI Network
if __name__ == "__main__":
    SSID = "Android"
    password = "12345678"
    connect_to_wifi(connection_callback, SSID, password)
