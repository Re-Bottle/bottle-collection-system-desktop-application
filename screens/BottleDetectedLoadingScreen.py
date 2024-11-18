import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from main import WIFI_STATE

from misc.utility import ApplicationState
from screens import HomeScreen, FinalScreen


def BottleDetectedLoadingScreen(window: tk.Tk, application_state: ApplicationState):
    back = Image.open("./assets/back.png")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=480,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    canvas.place(x=0, y=0)

    canvas.create_text(
        250.0,
        70.0,
        anchor="nw",
        text="Bottle detected, please wait...",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

    progress_bar = ttk.Progressbar(
        window,
        orient="horizontal",
        length=200,
        mode="indeterminate",
    )

    progress_bar.place(x=300, y=250)
    progress_bar.start()

    def load_final_screen():
        progress_bar.stop()  # Stop the progress bar animation
        FinalScreen.FinalScreen(window, application_state)  # Go to next screen

    window.after(5000, load_final_screen)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
