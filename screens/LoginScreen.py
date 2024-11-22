import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from components.keyboard import Add_Keyboard
from components.message_box import show_custom_error, show_custom_info

from misc.utility import (
    ApplicationState,
    validate_login_pass,
    load_passcode,
    save_passcode,
    hash_passcode,
)
from screens import HomeScreen, SettingsScreen

from main import WIFI_STATE


def on_login_button_click(
    login_pass, window: tk.Tk, application_state: ApplicationState
):
    """
    Handler for when the login button is clicked. Attempts to login
    and shows a success or error message.
    6 num password - 123456
    """
    if not validate_login_pass(login_pass):
        show_custom_error(
            "Invalid passcode",
            "Please check your credentials.",
            x=300,
            y=300,
        )
        return

    if verify_passcode(login_pass):
        show_custom_info(
            "Login Successful",
            "Successfully logged in!",
            x=300,
            y=300,
        )
        SettingsScreen.SettingsScreen(window, application_state)
    else:
        show_custom_error(
            "Connection Failed",
            "Failed to Login. Please check your credentials.",
            x=300,
            y=300,
        )


def verify_passcode(user_input: str):
    """Verify if the user input matches the stored hashed passcode"""
    # Load the hashed passcode stored in the registry
    stored_passcode = load_passcode()

    if stored_passcode is None:
        save_passcode("123456")
        # print("No passcode found in the registry. Default passcode can be used.")

    # Hash the user input and compare it with the stored hash
    hashed_input = hash_passcode(user_input)

    if hashed_input == stored_passcode:
        # print("Passcode verified successfully!")
        return True
    else:
        # print("Invalid passcode!")
        return False


def LoginScreen(window: tk.Tk, application_state: ApplicationState):
    # Load Images
    back = Image.open("./assets/back.png")
    login = Image.open("./assets/login.png")

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
        text=f"Passcode",
        font=("Arial", 16),
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
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
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    back_button.image = back_image
    back_button.bind(
        "<Button-1>",
        lambda _: HomeScreen.HomeScreen(window, application_state),
    )
    back_button.place(x=66, y=81)

    # Login button
    login_image = ImageTk.PhotoImage(login)
    login_button = tk.Label(
        window,
        image=login_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    login_button.bind(
        "<Button-1>",
        lambda _: on_login_button_click(passcode_var.get(), window, application_state),
    )
    login_button.image = login_image
    login_button.place(x=600, y=81)

    # Function for displaying keyboard
    Add_Keyboard(window, passcode_var, 6)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
