import tkinter as tk

from interface.io import control_servo, turn_on_led_test  # type: ignore
from interface.camera_interface import capture_image  # type: ignore
from interface.server_communicate import ping
from screens import HomeScreen
from misc.utility import ApplicationState
import platform


def on_escape(_):
    window.quit()


def setup():
    ping()  # to check connection to server

    # Test Code for IO
    if platform.system() == "Linux":
        # turn_on_led_test()
        # capture_image()
        # control_servo()
        pass

    pass


if __name__ == "__main__":

    setup()

    # Main Window
    window = tk.Tk()
    window.title("Bottle Collection System")
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
    window.geometry("800x480")
    window.configure(bg="#FFFFFF")
    window.bind("<Escape>", on_escape)  # type: ignore
    window.bind("<Button-2>", on_escape)  # type: ignore

    application_state = ApplicationState()
    HomeScreenCanvas = HomeScreen.HomeScreen(window, application_state)

    window.mainloop()
