import tkinter as tk
from tkinter import Canvas, messagebox, ttk
from PIL import Image, ImageTk

from main import WIFI_STATE

from screens import HomeScreen


def FinalScreen(window: tk.Tk, application_state: dict):
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")
    back_to_home = Image.open("./assets/back_to_home.png")
    qr_code = Image.open("./assets/qrcode_dummy.png")

    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)
    back_to_home_image = ImageTk.PhotoImage(back_to_home)
    qr_code_image = ImageTk.PhotoImage(qr_code)

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
        269.0,
        19.0,
        anchor="nw",
        text="Name | Logo",
        fill="#000000",
        font=("Kadwa Bold", 30),
    )

    canvas.create_text(
        701.0,
        15.0,
        anchor="nw",
        text=((application_state.get("WIFI")).value),
        fill="#515050",
        font=("Kadwa Regular", 10),
    )

    canvas.create_text(
        300.0,
        70.0,
        anchor="nw",
        text="Thank you!",
        fill="#515050",
        font=("Kadwa Regular", 20),
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
    canvas.image2 = connected_image
    canvas.image3 = not_connected_image

    back_to_home_image_button = tk.Label(
        window,
        image=back_to_home_image,
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )

    back_to_home_image_button.image = back_to_home_image
    back_to_home_image_button.bind(
        "<Button-1>",
        lambda _: HomeScreen.HomeScreen(window, application_state),
    )
    back_to_home_image_button.place(x=40, y=80)

    canvas.create_text(
        40.0,
        400.0,
        anchor="nw",
        text="Tap to start again!",
        fill="#000000",
        font=("Kadwa Regular", 15),
    )

    canvas.create_image(
        450,
        80,
        anchor=tk.NW,
        image=qr_code_image,
    )
    canvas.image5 = qr_code_image
    canvas.create_text(
        450.0,
        400.0,
        anchor="nw",
        text="Scan to verify your reward.",
        fill="#000000",
        font=("Kadwa Regular", 15),
    )

    return canvas
