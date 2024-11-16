import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from screens import SettingsScreen
from main import WIFI_STATE


def WiFiConnectScreen(window: tk.Tk, application_state: dict):
    # Load Images
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")
    settings = Image.open("./assets/settings.png")

    # Images for display
    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)
    settings_image = ImageTk.PhotoImage(settings)

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

    # Header text and labels
    canvas.create_text(
        269.0,
        19.0,
        anchor="nw",
        text="Wi-Fi Setup",
        fill="#000000",
        font=("Kadwa Bold", 40 * -1),
    )
    canvas.create_text(
        253.0,
        71.0,
        anchor="nw",
        text="Enter Wi-Fi Password",
        fill="#000000",
        font=("Kadwa Bold", 64 * -1),
    )
    canvas.create_text(
        170.0,
        150.0,
        anchor="nw",
        text="Please enter the Wi-Fi password below.",
        fill="#515050",
        font=("Kadwa Regular", 32 * -1),
    )

    # Entry field for Wi-Fi password input
    password_var = tk.StringVar()
    password_entry = tk.Entry(
        window,
        textvariable=password_var,
        font=("Arial", 16),
        width=20,
        show="*",  # Display password as asterisks
        bd=0,
        relief="flat",
        justify="center",
        bg="#FFFFFF",
    )
    password_entry.place(x=270, y=250)

    # Display Wi-Fi status
    canvas.create_text(
        701.0,
        15.0,
        anchor="nw",
        text=("Wi-Fi: " + (application_state.get("WIFI")).value),
        fill="#515050",
        font=("Kadwa Regular", 14 * -1),
    )
    canvas.create_image(
        677,
        10,
        anchor=tk.NW,
        image=(
            connected_image
            if application_state.get("WIFI") == WIFI_STATE.CONNECTED
            else not_connected_image
        ),
    )

    canvas.image1 = connected_image
    canvas.image2 = not_connected_image

    # Virtual Keyboard buttons (similar to previous example)
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
    ]

    def on_button_click(char):
        current_text = password_var.get()
        password_var.set(current_text + char)

    row, col = 1, 0
    for char in keyboard_buttons:
        button = tk.Button(
            window,
            text=char,
            width=5,
            height=2,
            font=("Arial", 12),
            command=lambda char=char: on_button_click(char),
        )
        button.place(x=30 + col * 60, y=350 + row * 50)
        col += 1
        if col > 9:  # New row after 10 buttons
            col = 0
            row += 1

    # Clear button to reset password entry
    clear_button = tk.Button(
        window,
        text="Clear",
        width=10,
        height=2,
        font=("Arial", 14),
        command=lambda: password_var.set(""),
    )
    clear_button.place(x=500, y=350)

    # Settings button to navigate to settings screen
    settings_button = tk.Label(
        window,
        image=settings_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    settings_button.image = settings_image
    settings_button.bind(
        "<Button-1>",
        lambda _: SettingsScreen.SettingsScreen(window, application_state),
    )
    settings_button.place(x=561, y=393)

    return canvas
