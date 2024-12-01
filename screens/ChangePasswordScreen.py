import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from components.message_box import show_custom_error, show_custom_info

from misc.utility import (
    ApplicationState,
    validate_login_pass,
    save_passcode,
)
from screens import HomeScreen, SettingsScreen

from main import WIFI_STATE


def on_update_button_click(
    new_pass, window: tk.Tk, application_state: ApplicationState
):
    """
    Handler for when the login button is clicked. Updates the default password to the one given by user.
    """
    if not validate_login_pass(new_pass):
        show_custom_error(
            "Invalid passcode",
            "Passcode must be a 6-digit number.",
            x=300,
            y=300,
        )
        return

    # Save the new passcode in the registry or file based on the OS
    save_passcode(new_pass)

    # Show success message
    show_custom_info(
        "Passcode Updated",
        "Passcode updated successfully!",
        x=300,
        y=300,
    )
    SettingsScreen.SettingsScreen(window, application_state)


def ChangePasswordScreen(window: tk.Tk, application_state: ApplicationState):
    # Load Images
    back = Image.open("./assets/back.png")
    update = Image.open("./assets/update.png")

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

    # Entry field for Wi-Fi passcode input
    passcode = tk.Label(
        window,
        text=f"Change Passcode",
        font=("Arial", 16),
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )
    passcode.place(x=115, y=150)
    passcode_var = tk.StringVar()

    passcode_entry = tk.Entry(
        window,
        textvariable=passcode_var,
        font=("Arial", 16),
        width=6,
        bd=0,
        relief="flat",
        justify="left",
        bg="#FFFFFF",
    )
    passcode_entry.place(x=120, y=200)

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

    # update password button
    update_image = ImageTk.PhotoImage(update)
    update_button = tk.Label(
        window,
        image=update_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    update_button.bind(
        "<Button-1>",
        lambda _: on_update_button_click(passcode_var.get(), window, application_state),
    )
    update_button.image = update_image
    update_button.place(x=600, y=81)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
