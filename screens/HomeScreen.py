import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from screens import SettingsScreen


def HomeScreen(window: tk.Tk):
    # Homescreen
    hero_image = Image.open("./assets/recycle.png")
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")
    settings = Image.open("./assets/settings.png")

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
        font=("Kadwa Bold", 40 * -1),
    )
    canvas.create_text(
        716.0,
        15.0,
        anchor="nw",
        text="Connected",
        fill="#515050",
        font=("Kadwa Regular", 14 * -1),
    )

    canvas.create_text(
        253.0,
        71.0,
        anchor="nw",
        text="Welcome",
        fill="#000000",
        font=("Kadwa Bold", 64 * -1),
    )
    canvas.create_text(
        170.0,
        150.0,
        anchor="nw",
        text="to the bottle collection system",
        fill="#000000",
        font=("Kadwa Regular", 32 * -1),
    )
    canvas.create_text(
        323.0,
        249.0,
        anchor="nw",
        text="Please insert a recyclable bottle to start ...",
        fill="#515050",
        font=("Kadwa Regular", 24 * -1),
    )

    # Images
    recycle_image = ImageTk.PhotoImage(hero_image)
    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)
    settings_image = ImageTk.PhotoImage(settings)

    canvas.create_image(117, 203, anchor=tk.NW, image=recycle_image)
    canvas.create_image(692, 10, anchor=tk.NW, image=connected_image)

    canvas.image1 = recycle_image
    canvas.image2 = connected_image
    canvas.image3 = not_connected_image

    # Settings button
    settings_button = tk.Button(
        window,
        image=settings_image,
        command=lambda: SettingsScreen.SettingsScreen(window),
    )
    settings_button.image = settings_image
    settings_button.place(x=561, y=393)

    return canvas
