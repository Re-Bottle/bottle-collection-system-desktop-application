import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from misc.utility import ApplicationState, validate_login_pass
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
        messagebox.showerror(
            "Invalid passcode",
            f"Please check your credentials.",
        )
        return

    success = login_pass == "123456"

    # Show appropriate message box
    if success:
        messagebox.showinfo(
            "Login Successful",
            f"Successfully logged in!",
        )

        SettingsScreen.SettingsScreen(window, application_state)

    else:
        messagebox.showerror(
            "Connection Failed",
            f"Failed to Login. Please check your credentials.",
        )


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

    shift_active = False  # Track shift state

    def on_button_click(char):
        # Check if shift is active and make the letter uppercase (alphabet characters only)
        if shift_active and char.isalpha():
            char = char.upper()
        current_text = passcode_var.get()
        passcode_var.set(current_text + char)

    def toggle_shift():
        nonlocal shift_active
        shift_active = not shift_active
        shift_button.config(bg="#93B15A" if shift_active else "#FFFFFF")

    row, col = 1, 0
    for char in keyboard_buttons:
        if char != "shift":  # Only create button for characters, not for "shift"
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
            if col > 13:  # New row after 13 buttons
                col = 0
                row += 1

    # Shift button to toggle between lower and upper case
    shift_button = tk.Button(
        window,
        text="Shift",
        width=4,
        height=1,
        font=("Arial", 12),
        command=toggle_shift,  # Toggle shift state when clicked
        bg="#FFFFFF",
    )
    shift_button.place(x=30 + col * 55, y=230 + row * 40)
    col += 1

    # backspace
    def backspace():
        current_passcode = passcode_var.get()  # Get the current passcode
        if len(current_passcode) > 0:
            # Remove the last character of the passcode
            new_passcode = current_passcode[:-1]
            passcode_var.set(new_passcode)

    backspace_button = tk.Button(
        window, text="←", width=4, height=1, font=("Arial", 12), command=backspace
    )
    backspace_button.place(x=30 + (col) * 55, y=230 + row * 40)

    # Clear button to reset passcode entry
    clear_button = tk.Button(
        window,
        text="Clear",
        width=4,
        height=1,
        font=("Arial", 12),
        command=lambda: passcode_var.set(""),
    )
    clear_button.place(x=30 + (col + 1) * 55, y=230 + row * 40)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
