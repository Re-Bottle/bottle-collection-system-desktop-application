import tkinter as tk

from interface.io_check import turn_on_led_test
from screens import HomeScreen
from misc.utility import ApplicationState
from interface.io_check import turn_on_led_test
import platform


def on_escape(_):
    window.quit()


if __name__ == "__main__":
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

    # Test Code for IO
    if platform.system() == "Linux":
        turn_on_led_test()

    window.mainloop()
