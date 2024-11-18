from enum import Enum
import os
import subprocess
import platform
import time


class WIFI_STATE(Enum):
    CONNECTED = "Connected"
    NOT_CONNECTED = "Not Connected"
    UNAVAILABLE = "Unavailable"


class ApplicationState:
    wifi_state: WIFI_STATE = WIFI_STATE.NOT_CONNECTED

    def __init__(self):
        self.update_wifi_state()

    def set_wifi_state(self, state: WIFI_STATE):
        self.wifi_state = state

    def get_wifi_state(self):
        return self.wifi_state

    def update_wifi_state(self):
        state = get_wifi_state()
        if state:
            self.set_wifi_state(WIFI_STATE.CONNECTED)
        elif state is False:
            self.set_wifi_state(WIFI_STATE.NOT_CONNECTED)
        else:
            self.set_wifi_state(WIFI_STATE.UNAVAILABLE)


def connect_wifi(ssid, password):
    """
    Connect to a Wi-Fi network based on the current operating system.

    :param ssid: The Wi-Fi network name (SSID).
    :param password: The Wi-Fi network password.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        connect_wifi_windows(ssid, ssid, password)
    elif current_os == "linux":
        connect_wifi_linux(ssid, password)
    else:
        print(f"Operating system '{current_os}' not supported for Wi-Fi connection.")


def connect_wifi_windows(name, SSID, password):
    # function to establish a new connection
    config = (
        """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""
        + name
        + """</name>
    <SSIDConfig>
        <SSID>
            <name>"""
        + SSID
        + """</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""
        + password
        + """</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    )
    disconnect_command = "netsh wlan disconnect"
    command = 'netsh wlan add profile filename="' + name + '.xml"' + " interface=WiFi"
    with open(name + ".xml", "w") as file:
        file.write(config)
    os.system(disconnect_command)
    os.system(command)


def connect_wifi_linux(ssid, password):
    """
    Connect to a Wi-Fi network on Linux using nmcli (NetworkManager).

    :param ssid: The Wi-Fi network name (SSID).
    :param password: The Wi-Fi network password.
    """
    try:
        # First, check if the network is available
        subprocess.run(
            ["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True
        )
        print(f"Successfully connected to {ssid}!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {ssid}: {e}")


def list_available_wifi(should_refresh=True):
    """
    List all available Wi-Fi networks based on the current operating system.
    Returns a list of dictionaries containing SSID (network name) and signal strength.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        return list_available_wifi_windows(should_refresh)
    elif current_os == "linux":
        return list_available_wifi_linux(should_refresh)
    else:
        print(f"Operating system '{current_os}' not supported for Wi-Fi scanning.")
        return []


def list_available_wifi_windows(should_refresh=True):
    """
    List all available Wi-Fi networks on Windows using the `netsh` command.
    Returns a list of SSIDs and signal strength.
    """
    try:
        if should_refresh:
            subprocess.run(
                ["wifi", "scan"],
                check=True,
                text=True,
                stdout=subprocess.DEVNULL,  # Suppress standard output
                stderr=subprocess.DEVNULL,  # Suppress standard error
            )
            time.sleep(5)  # Wait a few seconds to ensure the scan is complete

        # Run `netsh wlan show networks` to get available Wi-Fi networks
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "networks"], text=True
        )

        networks = []

        for result_item in result.strip().splitlines():
            if "SSID" in result_item:
                network_name = result_item.split(":")[-1].strip()
                if network_name:
                    networks.append(network_name)

        return networks

    except subprocess.CalledProcessError as e:
        print(f"Error listing Wi-Fi networks on Windows: {e}")
        return []


def list_available_wifi_linux(should_refresh=True):
    """
    List all available Wi-Fi networks on Linux using the `nmcli` command.
    Returns a list of SSIDs and signal strength.
    """
    try:
        # Run `nmcli dev wifi list` to get available Wi-Fi networks
        result = subprocess.check_output(
            ["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"], text=True
        )

        # Parse the result to extract SSIDs and signal strength
        networks = []
        for line in result.splitlines():
            ssid, signal = line.split(":")
            networks.append({"SSID": ssid, "Signal Strength": signal})

        return networks

    except subprocess.CalledProcessError as e:
        print(f"Error listing Wi-Fi networks on Linux: {e}")
        return []


def get_wifi_state():
    """
    Get the current Wi-Fi connection status based on the operating system.
    Returns True if connected, False if not connected, and None if the state could not be determined.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        return get_wifi_state_windows()
    elif current_os == "linux":
        return get_wifi_state_linux()
    else:
        print(
            f"Operating system '{current_os}' not supported for Wi-Fi state checking."
        )
        return None


def get_wifi_state_windows():
    try:
        # Run netsh command to show WLAN interfaces
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            check=True,
            text=True,
            capture_output=True,
        )
        return "State" in result.stdout and not "disconnected" in result.stdout.lower()
    except subprocess.CalledProcessError:
        print("Error checking Wi-Fi state.")
        return False


def get_wifi_state_linux():
    try:
        # Run nmcli command to check Wi-Fi connection status
        result = subprocess.run(
            ["nmcli", "-t", "-f", "ACTIVE,SSID", "device", "wifi"],
            check=True,
            text=True,
            capture_output=True,
        )
        if "yes" in result.stdout.lower():
            print("Connected to Wi-Fi.")
            return True
        else:
            print("Not connected to Wi-Fi.")
            return False
    except subprocess.CalledProcessError:
        print("Error checking Wi-Fi state.")
        return False


def restart():
    """
    Restart the system based on the current operating system.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        restart_windows()
    elif current_os == "linux":
        # restart_linux()
        pass
    else:
        print(f"Operating system '{current_os}' not supported for system restart.")


def restart_windows():
    """Restart the system on Windows."""
    print("Restarting the system...")
    subprocess.run(["shutdown", "/r", "/t", "0"])  # /r = restart, /t 0 = no delay


# Example usage:
if __name__ == "__main__":
    available_networks = list_available_wifi()
    if available_networks:
        for network in available_networks:
            print(f"SSID: {network}")
    else:
        print("No Wi-Fi networks found.")
