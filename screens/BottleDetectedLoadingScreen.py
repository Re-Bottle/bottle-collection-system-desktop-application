import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk

from main import WIFI_STATE

from screens import HomeScreen, FinalScreen


def BottleDetectedLoadingScreen(window: tk.Tk, application_state: dict):
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
        250.0,
        70.0,
        anchor="nw",
        text="Bottle detected, please wait...",
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

    progress_bar = ttk.Progressbar(
        window,
        orient="horizontal",
        length=200,
        mode="indeterminate",
    )
    progress_bar.place(x=300, y=250)
    progress_bar.start()

    def load_final_screen():
        progress_bar.stop()  # Stop the progress bar animation
        FinalScreen.FinalScreen(window, application_state)  # Go to next screen

    window.after(
        5000, load_final_screen
    )  # (just for simulation) Wait for 5 seconds before going to the next screen

    return canvas
