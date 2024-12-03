import tkinter as tk
from tkinter import Canvas

from components.date_time import Add_date_time
from components.device_reg_status import Add_Device_Reg_Status
from components.keyboard import Add_Keyboard
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from components.message_box import show_custom_error, show_custom_info

from misc.utility import ApplicationState, validate_login_pass, verify_passcode
from screens import HomeScreen, SettingsScreen


def on_login_button_click(
    login_pass: str, window: tk.Tk, application_state: ApplicationState
):
    """
    Handler for when the login button is clicked. Attempts to login
    and shows a success or error message.
    6 num password - 123456
    """
    if not validate_login_pass(login_pass):
        show_custom_error(
            window,
            "Invalid passcode",
            "Please check your credentials.",
            x=300,
            y=300,
        )
        return False

    if verify_passcode(login_pass):
        show_custom_info(
            window,
            "Login Successful",
            "Successfully logged in!",
            x=300,
            y=300,
        )
        SettingsScreen.SettingsScreen(window, application_state)
    else:
        show_custom_error(
            window,
            "Connection Failed",
            "Failed to Login. Please check your credentials.",
            x=300,
            y=300,
        )


def LoginScreen(window: tk.Tk, application_state: ApplicationState):

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
        relief="solid",
        justify="left",
        bg="#FFFFFF",
    )
    passcode_entry.place(x=120, y=200)

    back_image = tk.PhotoImage(file="./assets/back.png")
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
    back_button.image = back_image  # type: ignore as we are doing this to keep reference to image
    back_button.bind(
        "<Button-1>",
        lambda _: HomeScreen.HomeScreen(window, application_state),
    )
    back_button.place(x=66, y=81)

    # Login button
    login_image = tk.PhotoImage(file="./assets/login.png")
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
    login_button.image = login_image  # type: ignore as we are doing this to keep reference to image
    login_button.place(x=600, y=81)

    # Function for displaying keyboard
    Add_Keyboard(window, passcode_var, 6)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    Add_Device_Reg_Status(canvas, application_state)

    return canvas
