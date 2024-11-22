import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from screens import SettingsScreen

from misc.utility import ApplicationState, list_available_wifi
from main import WIFI_STATE

uniqueID = "1234567890"
is_disabled = False


def RegisterDeviceScreen(window: tk.Tk, application_state: ApplicationState):
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
        210.0,
        240.0,
        anchor="nw",
        text="Unique ID for your device is:",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

    canvas.create_text(
        300.0,
        290.0,
        anchor="nw",
        text=uniqueID,
        fill="#93B15A",
        font=("Kadwa Regular", 20),
    )

    # Back button to go to Settings screen
    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Label(
        window,
        image=back_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    back_button.bind(
        "<Button-1>",
        lambda _: (
            SettingsScreen.SettingsScreen(window, application_state)
            if not is_disabled
            else None
        ),
    )
    back_button.image = back_image
    back_button.place(x=66, y=81)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
