import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from main import WIFI_STATE

# from screens import HomeScreen


def LoginScreen(window: tk.Tk):
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")
    back = Image.open("./assets/back.png")

    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)

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
        177.0,
        155.0,
        anchor="nw",
        text="Bottle detected, please wait...",
        fill="#515050",
        font=("Kadwa Regular", 32),
    )

    # wifi connected image
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

    # back button
    back_image = ImageTk.PhotoImage(back)
    # back_button = tk.Button(
    #     window,
    #     image=back_image,
    #     command=lambda: SelectWiFiScreen.SelectWiFiScreen(window),
    # )
    # back_button.image = back_image
    # back_button.place(x=66, y=81)

    # login entry fields
    # keyboard for input

    return canvas
