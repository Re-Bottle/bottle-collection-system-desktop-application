import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from components.message_box import show_custom_error, show_custom_info

from misc.utility import ApplicationState, connect_wifi, validate_wifi_credentials
from screens import ConfigureWiFiScreen

from main import WIFI_STATE


def on_connect_button_click(wifi_name, password):
    """
    Handler for when the connect button is clicked. Attempts to connect to the Wi-Fi
    and shows a success or error message.
    """
    # Call the connect_wifi function and check the result
    if not validate_wifi_credentials(wifi_name, password):
        show_custom_error(
            "Invalid Credentials",
            "Please check your credentials.",
            x=300,
            y=300,
        )
        return
    success = connect_wifi(wifi_name, password)

    # Show appropriate message box
    if success:

        show_custom_info(
            "Connection Successful",
            f"Successfully connected to {wifi_name}!",
            x=300,
            y=300,
        )
    else:
        show_custom_error(
            "Connection Failed",
            f"Failed to connect to {wifi_name}. Please check your credentials.",
            x=300,
            y=300,
        )


def WiFiConnectScreen(
    window: tk.Tk, application_state: ApplicationState, wifi_name: str = ""
):
    # Load Images
    back = Image.open("./assets/back.png")
    connect = Image.open("./assets/connect.png")

    # Create Canvas for layout
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

    # Entry field for Wi-Fi password input
    password = tk.Label(
        window,
        text=f"Password ({wifi_name})",
        font=("Arial", 16),
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )
    password.place(x=115, y=150)
    password_var = tk.StringVar()

    password_entry = tk.Entry(
        window,
        textvariable=password_var,
        font=("Arial", 16),
        width=64,
        bd=0,
        relief="flat",
        justify="left",
        bg="#FFFFFF",
    )
    password_entry.place(x=120, y=200)

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
        lambda _: ConfigureWiFiScreen.ConfigureWIFIScreen(window, application_state),
    )
    back_button.place(x=66, y=81)

    # Connect button
    connect_image = ImageTk.PhotoImage(connect)
    connect_button = tk.Label(
        window,
        image=connect_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    connect_button.bind(
        "<Button-1>",
        lambda _: on_connect_button_click(wifi_name, password_var.get()),
    )
    connect_button.image = connect_image
    connect_button.place(x=600, y=81)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
