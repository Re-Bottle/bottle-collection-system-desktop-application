from enum import Enum
import os
import subprocess
import platform
import time
import hashlib
import keyring
from typing import List
import re
import uuid


DEFAULT_PASSWORD = "123456"
PASSCODE_SERVICE_NAME = "Passcode"
DEVICE_SERVICE_NAME = "device"
REGISTRATION_SERVICE_NAME = "registration"
OWNER_ID_NAME = "ownerId"
USER_NAME = "Re-Bottle"


class WIFI_STATE(Enum):
    CONNECTED = "Connected"
    NOT_CONNECTED = "Not Connected"
    UNAVAILABLE = "Unavailable"


class REGISTRATION_STATE(Enum):
    REGISTERED = "Registered"
    UNREGISTERED = "Unregistered"


class ApplicationState:
    wifi_state: WIFI_STATE = WIFI_STATE.NOT_CONNECTED
    device_registration_state: REGISTRATION_STATE = REGISTRATION_STATE.UNREGISTERED
    owner_id: str = ""
    device_id: str = ""
    claimed_at: str = ""

    def __init__(self):
        self.update_wifi_state()
        self.load_device_registration_state()

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

    def load_device_registration_state(self):
        # TODO: Load Device Registration State

        pass


def generate_UUID() -> str:
    return str(uuid.uuid4())


def validate_login_pass(login_pass: str) -> bool:
    """
    Validates the login password.
    Basic requirements are:
        length should be 5
        only numbers
    """
    if not login_pass:
        return False
    if len(login_pass) != 6:
        return False
    if not login_pass.isdigit():
        return False
    return True


def validate_wifi_credentials(ssid: str, password: str) -> bool:
    """
    Validate the Wi-Fi credentials by checking if the SSID and password are not empty,
    if they meet basic length and character requirements, and if the password is complex enough.
    """
    # Check if SSID is empty
    if not ssid:
        return False

    # Check if password is empty
    if not password:
        return False

    # Check if SSID length is within acceptable range (1 to 32 characters is standard for Wi-Fi)
    if len(ssid) < 1 or len(ssid) > 32:
        return False

    # Check if password length is within acceptable range (minimum 8 characters for WPA2)
    if len(password) < 8 or len(password) > 63:
        return False

    # Validate SSID for valid characters (only alphanumeric and special characters like -_ are typically allowed)
    if not re.match(r"^[a-zA-Z0-9\-_ ']+$", ssid):
        return False

    # If all checks pass, return True
    return True


def connect_wifi(ssid: str, password: str) -> bool | None:
    """
    Connect to a Wi-Fi network based on the current operating system.

    :param ssid: The Wi-Fi network name (SSID).
    :param password: The Wi-Fi network password.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        return connect_wifi_windows(ssid, ssid, password)
    elif current_os == "linux":
        return connect_wifi_linux(ssid, password)
    else:
        return False


def connect_wifi_windows(name: str, SSID: str, password: str):
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
    connect_command = "netsh wlan connect name=" + name

    with open(name + ".xml", "w") as file:
        file.write(config)
    try:
        os.system(command)
        os.system(disconnect_command)
        subprocess.run(connect_command, check=True, shell=True)
        return get_wifi_state(True)
    except subprocess.CalledProcessError as _:
        return False


def connect_wifi_linux(ssid: str, password: str):
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
        return True
    except subprocess.CalledProcessError as _:
        return False


def list_available_wifi(should_refresh: bool = True) -> List[str]:
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


def list_available_wifi_windows(should_refresh: bool = True) -> List[str]:
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

        networks: List[str] = []

        for result_item in result.strip().splitlines():
            if "SSID" in result_item:
                network_name = result_item.split(":")[-1].strip()
                if network_name:
                    networks.append(network_name)

        return networks

    except subprocess.CalledProcessError as e:
        print(f"Error listing Wi-Fi networks on Windows: {e}")
        return []


def list_available_wifi_linux(should_refresh: bool = True) -> List[str]:
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
        networks: List[str] = []
        for line in result.splitlines():
            ssid, _ = line.split(":")
            networks.append(ssid)

        return networks

    except subprocess.CalledProcessError as e:
        print(f"Error listing Wi-Fi networks on Linux: {e}")
        return []


def get_wifi_state(should_delay: bool = False) -> bool:
    """
    Get the current Wi-Fi connection status based on the operating system.
    Returns True if connected, False if not connected, and None if the state could not be determined.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        return get_wifi_state_windows(should_delay)
    elif current_os == "linux":
        return get_wifi_state_linux()
    else:
        print(
            f"Operating system '{current_os}' not supported for Wi-Fi state checking."
        )
        return False


def get_wifi_state_windows(should_delay: bool = False):
    if should_delay:
        time.sleep(5)
    try:
        # Run netsh command to show WLAN interfaces
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            check=True,
            text=True,
            capture_output=True,
        )
        return "State" in result.stdout and not (
            "disconnected" in result.stdout.lower()
            or "authenticating" in result.stdout.lower()
            or "associating" in result.stdout.lower()
        )
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


def save_passcode_to_registry(passcode: str, name: str = PASSCODE_SERVICE_NAME):
    """
    Save hashed passcode in the Windows registry
    Create a registry key under HKEY_CURRENT_USER\\Software\\MyApp
    Set the hashed passcode under the "Passcode" name
    """
    import winreg

    try:
        hashed_passcode = hash_password(passcode)

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\MyApp")
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, hashed_passcode)
        winreg.CloseKey(key)
        print("Hashed passcode saved successfully in the registry.")
    except Exception as e:
        print(f"Failed to save passcode to registry: {e}")


def load_passcode_from_registry(name: str = PASSCODE_SERVICE_NAME):
    """
    Load passcode from the Windows registry
    Open the registry key where the passcode is stored
    Read the passcode value
    If the registry key doesn't exist, return None
    Close the registry key
    """
    import winreg

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\MyApp")
        passcode, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return passcode
    except FileNotFoundError:
        return None  # If the registry key doesn't exist, return None
    except Exception as e:
        print(f"Failed to load passcode from registry: {e}")
        return None


def load_data_from_keyring(SERVICE_NAME: str = PASSCODE_SERVICE_NAME):
    """Load value from the keyring."""
    return keyring.get_password(SERVICE_NAME, USER_NAME)


# Called by Login screen if the user wants to access settings
def verify_passcode(user_input: str):
    """Verify if the user input hash matches the stored hashed passcode"""
    if platform.system().lower() == "windows":
        stored_passcode = load_passcode_from_registry()

        if stored_passcode is None:
            save_passcode(DEFAULT_PASSWORD)
        return hash_password(user_input) == stored_passcode

    else:
        stored_hashed_password = (
            load_data_from_keyring()
        )  # None if password no Set or default password used

        if stored_hashed_password is None:
            stored_hashed_password = initialize_password_linux()
            print(f"stored hash was None and new Hash is {stored_hashed_password}")

        return hash_password(user_input) == stored_hashed_password


def hash_password(password: str):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def initialize_password_linux():
    """Initialize password if it doesn't exist."""
    hashed_password = hash_password(DEFAULT_PASSWORD)
    keyring.set_password(PASSCODE_SERVICE_NAME, USER_NAME, hashed_password)
    print("Password initialized with default value.")
    return hashed_password


def initialize_device() -> str:
    """Initialize password if it doesn't exist."""
    print("Initializing device...")
    device_id = str(uuid.uuid4())
    keyring.set_password(DEVICE_SERVICE_NAME, USER_NAME, device_id)
    print(f"Device Initialized with id {device_id}")
    return device_id


def get_device_id():
    """Get the device id from the keyring."""
    device_id = load_data_from_keyring(DEVICE_SERVICE_NAME)
    if device_id == "" or device_id is None:
        device_id = initialize_device()
    return device_id

def get_device_details() -> REGISTRATION_STATE:
    '''Get the device registration state from the keyring'''
    registration_state = load_data_from_keyring(REGISTRATION_SERVICE_NAME)
    if registration_state is None:
        keyring.set_password(REGISTRATION_SERVICE_NAME, USER_NAME, REGISTRATION_STATE.UNREGISTERED.value)
    return REGISTRATION_STATE(registration_state)


def update_password_linux(new_password: str):
    """Update the stored password."""
    stored_password = load_data_from_keyring()
    if stored_password is None:
        initialize_password_linux()
    hashed_password = hash_password(new_password)
    keyring.set_password(PASSCODE_SERVICE_NAME, USER_NAME, hashed_password)
    print("Password updated successfully.")


def save_passcode(passcode: str):
    if platform.system().lower() == "windows":
        save_passcode_to_registry(passcode)
    else:
        update_password_linux(passcode)


# Example usage:
if __name__ == "__main__":
    available_networks = list_available_wifi()
    if available_networks:
        for network in available_networks:
            print(f"SSID: {network}")
    else:
        print("No Wi-Fi networks found.")
