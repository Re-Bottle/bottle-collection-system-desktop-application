import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from misc.utility import ApplicationState
from screens import ConfigureWiFiScreen

from main import WIFI_STATE


def WiFiConnectScreen(
    window: tk.Tk, application_state: ApplicationState, wifi_name: str = ""
):
    # Load Images
    settings = Image.open("./assets/settings.png")
    back = Image.open("./assets/back.png")

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
        # show="*",  # Display password as asterisks
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

    # Virtual Keyboard buttons
    keyboard_buttons = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
        "o",
        "p",
        "a",
        "s",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "z",
        "x",
        "c",
        "v",
        "b",
        "n",
        "m",
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "_",
        "+",
        "-",
        "=",
        "[",
        "]",
        "{",
        "}",
        "|",
        ";",
        ":",
        "'",
        '"',
        ",",
        ".",
        "<",
        ">",
        "/",
        "?",
        "shift",
    ]

    def on_button_click(char):
        current_text = password_var.get()
        password_var.set(current_text + char)

    row, col = 1, 0
    for char in keyboard_buttons:
        button = tk.Button(
            window,
            text=char,
            width=4,
            height=1,
            font=("Arial", 12),
            command=lambda char=char: on_button_click(char),
        )
        button.place(x=30 + col * 55, y=230 + row * 40)
        col += 1
        if col > 13:  # New row after 10 buttons
            col = 0
            row += 1
    # backspce
    backspace_button = tk.Button(
        window,
        text="←",
        width=4,
        height=1,
        font=("Arial", 12),
        command=lambda: password_var.set(""),
    )
    backspace_button.place(x=30 + (col) * 55, y=230 + row * 40)

    # Clear button to reset password entry
    clear_button = tk.Button(
        window,
        text="Clear",
        width=4,
        height=1,
        font=("Arial", 12),
        command=lambda: password_var.set(""),
    )
    clear_button.place(x=30 + (col + 1) * 55, y=230 + row * 40)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
