import tkinter as tk
from PIL import Image, ImageTk

from misc.utility import WIFI_STATE, ApplicationState


def Add_Wifi_Status(canvas: tk.Canvas, application_state: ApplicationState):
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")

    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)

    canvas.create_text(
        701.0,
        15.0,
        anchor="nw",
        text=(application_state.get_wifi_state().value),
        fill="#515050",
        font=("Kadwa Regular", 10),
    )

    canvas.create_image(
        677,
        10,
        anchor=tk.NW,
        image=(
            connected_image
            if application_state.get_wifi_state() == WIFI_STATE.CONNECTED
            else not_connected_image
        ),
    )

    canvas.image2 = connected_image
    canvas.image3 = not_connected_image
