import tkinter as tk

from interface.io import control_servo, turn_on_led_test  # type: ignore
from interface.camera_interface import capture_image  # type: ignore
from interface.server_communicate import get_registration_status
# from interface.custom_data_send import notify_bottle_detected
from screens import HomeScreen
from misc.utility import OWNER_ID_NAME, REGISTRATION_STATE, ApplicationState, get_device_id, get_device_details, load_data_from_keyring
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


if __name__ == "__main__":

    setup()  # Setup code for the application

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

    HomeScreenCanvas = HomeScreen.HomeScreen(window, application_state)

    window.mainloop()
