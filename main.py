import tkinter as tk
import threading
from interface.custom_data_send import subscribe_mqtt
from interface.io import control_servo, turn_on_led_test  # type: ignore
from interface.camera_interface import capture_image  # type: ignore
from interface.server_communicate import get_registration_status

# from interface.custom_data_send import main
from screens import BottleDetectedLoadingScreen, HomeScreen
from misc.utility import (
    OWNER_ID_NAME,
    REGISTRATION_STATE,
    ApplicationState,
    get_device_id,
    get_device_details,
    load_data_from_keyring,
)
import platform

application_state = ApplicationState()


def on_escape(_):
    window.quit()


def setup():
    application_state.device_id = get_device_id()
    application_state.device_registration_state = get_device_details()
    if application_state.device_registration_state == REGISTRATION_STATE.UNREGISTERED:
        response = get_registration_status(application_state.device_id)
        # application_state.device_registration_state = response.isRegistered
        application_state.owner_id = response.owner_id
        # notify_bottle_detected(application_state.device_id)
    else:
        # load owner id  from the keyring
        op = load_data_from_keyring(OWNER_ID_NAME)
        if op is not None:
            application_state.owner_id = op
        pass

    # Test Code for IO
    if platform.system() == "Linux":
        # turn_on_led_test()
        # capture_image()
        # control_servo()
        pass

    pass


def start_mqtt_listener():
    """Start the MQTT subscription in a separate daemon thread."""
    try:
        mqtt_thread = threading.Thread(
            target=subscribe_mqtt, args=(application_state.device_id,), daemon=True
        )
        mqtt_thread.start()
    except Exception as e:
        print(f"Error starting MQTT thread: {e}")


# Only for simulation
def go_to_bottle_detected_screen():
    BottleDetectedLoadingScreen.BottleDetectedLoadingScreen(window, application_state)


if __name__ == "__main__":

    setup()
    # start_mqtt_listener()

    # Main Window
    window = tk.Tk()
    window.title("Bottle Collection System")
    window.resizable(False, False)
    window.attributes("-fullscreen", True)  # type: ignore
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
    window.geometry("800x480")
    window.configure(bg="#FFFFFF")
    window.bind("<Escape>", on_escape)  # type: ignore
    window.bind("<Button-2>", on_escape)  # type: ignore
    window.bind("<Button-3>", lambda event: go_to_bottle_detected_screen())

    HomeScreenCanvas = HomeScreen.HomeScreen(window, application_state)

    window.mainloop()
