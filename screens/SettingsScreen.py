import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status

from misc.utility import ApplicationState, restart
from screens import HomeScreen, ConfigureWiFiScreen, BottleDetectedLoadingScreen


def SettingsScreen(window: tk.Tk, application_state: ApplicationState):
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
        340.0,
        70.0,
        anchor="nw",
        text="Settings",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

    # card
    card_x1, card_y1 = 150, 172
    card_width, card_height = 500, 200
    card_x2, card_y2 = card_x1 + card_width, card_y1 + card_height

    canvas.create_rectangle(
        card_x1, card_y1, card_x2, card_y2, fill="#ffffff", outline="#000000", width=2
    )

    # Buttons
    # Configure WiFi
    button_configure_wifi = tk.Label(
        window,
        text="> Configure WiFi",
    )
    button_configure_wifi.bind(
        "<Button-1>",
        lambda _: ConfigureWiFiScreen.ConfigureWIFIScreen(window, application_state),
    )
    button_configure_wifi.place(x=163, y=205)

    # Restart Device
    button_restart = tk.Label(
        window,
        text="> Restart",
    )
    button_restart.bind("<Button-1>", lambda _: restart())
    button_restart.place(x=163, y=255)

    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Label(
        window,
        image=back_image,
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )
    back_button.image = back_image
    back_button.bind(
        "<Button-1>",
        lambda _: HomeScreen.HomeScreen(window, application_state),
    )
    back_button.place(x=66, y=81)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
