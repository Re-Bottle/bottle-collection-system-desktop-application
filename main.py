import tkinter as tk
from screens import HomeScreen
from utility import WIFI_STATE

from screens import WiFiConnectScreen  # TODO:to test wifiConnectScreen, remove


def on_escape(event=None):
    window.quit()


# TODO: delete this function
def on_k_key(event=None):
    WiFiConnectScreen.WiFiConnectScreen(
        window, application_state
    )  # Assuming this function exists


application_state = {"WIFI": WIFI_STATE.NOT_CONNECTED}

if __name__ == "__main__":
    # Main Window
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("800x480")
    window.configure(bg="#FFFFFF")
    window.title("Bottle Collection System")
    window.bind("<Escape>", on_escape)

    # TODO: remove this line
    window.bind("k", on_k_key)  # When "K" is pressed, go to WiFiConnectScreen

    HomeScreenCanvas = HomeScreen.HomeScreen(window, application_state)

    window.mainloop()
