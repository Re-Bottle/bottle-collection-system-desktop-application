import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

# import boto3
# import os

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from screens import SettingsScreen

from misc.utility import ApplicationState


# This function handles to the reload and check if device is registered when the refresh button is clicked
def refresh_button_handler(canvas: tk.Canvas, window: tk.Tk):

    return


def get_device_id():
    # TODO: implement this function
    return "getting device id.... please wait"


def RegisterDeviceScreen(window: tk.Tk, application_state: ApplicationState):
    refresh = Image.open("./assets/reload.png")
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
        text=get_device_id(),
        fill="#93B15A",
        font=("Kadwa Regular", 20),
    )

    # Back button to go to Settings screen
    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Label(
        window,
        image=back_image,  # type: ignore
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    back_button.bind(
        "<Button-1>",
        lambda _: (SettingsScreen.SettingsScreen(window, application_state)),
    )
    back_button.image = back_image  # type: ignore as we are doing this to keep reference to image
    back_button.place(x=66, y=81)

    # Refresh Button
    refresh_image = ImageTk.PhotoImage(refresh)
    refresh_button = tk.Label(
        window,
        image=refresh_image,  # type: ignore
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    refresh_button.bind(
        "<Button-1>",
        lambda _: refresh_button_handler(canvas, window),
    )
    refresh_button.image = refresh_image  # type: ignore as we are doing this to keep reference to image
    refresh_button.place(x=700, y=81)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
