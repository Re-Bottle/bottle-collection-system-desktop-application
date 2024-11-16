import tkinter as tk
from screens import HomeScreen
from utility import WIFI_STATE


def on_escape(event=None):
    window.quit()


application_state = {"WIFI": WIFI_STATE.NOT_CONNECTED}

if __name__ == "__main__":
    # Main Window
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("800x480")
    window.configure(bg="#FFFFFF")
    window.title("Bottle Collection System")
    window.bind("<Escape>", on_escape)

    HomeScreenCanvas = HomeScreen.HomeScreen(window, application_state)

    window.mainloop()