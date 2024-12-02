import tkinter as tk
from screens import BottleDetectedLoadingScreen, HomeScreen
from misc.utility import WIFI_STATE, ApplicationState


def on_escape(event=None):
    window.quit()


if __name__ == "__main__":
    # Main Window
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("800x480")
    window.configure(bg="#FFFFFF")
    window.title("Bottle Collection System")
    window.bind("<Escape>", on_escape)
    window.bind("<Button-2>", on_escape)

    application_state = ApplicationState()
    HomeScreenCanvas = HomeScreen.HomeScreen(window, application_state)

    window.mainloop()
