import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from screens import HomeScreen, SelectWiFiScreen


def SettingsScreen(window: tk.Tk):
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")
    back = Image.open("./assets/back.png")

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

    # images
    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)

    canvas.create_image(692, 10, anchor=tk.NW, image=connected_image)

    canvas.image2 = connected_image
    canvas.image3 = not_connected_image

    # card
    card_x1, card_y1 = 150, 172
    card_width, card_height = 500, 200
    card_x2, card_y2 = card_x1 + card_width, card_y1 + card_height

    canvas.create_rectangle(
        card_x1, card_y1, card_x2, card_y2, fill="#ffffff", outline="#000000", width=2
    )

    # buttons
    button_configure_wifi = tk.Button(
        window,
        text="> Configure WiFi",
        command=lambda: SelectWiFiScreen.SelectWiFiScreen(window),
    )
    button_configure_wifi.place(x=163, y=205)

    button_restart = tk.Button(
        window, text="> Restart", command=lambda: print("Option 2 Selected")
    )
    button_restart.place(x=163, y=255)

    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Button(
        window, image=back_image, command=lambda: HomeScreen.HomeScreen(window)
    )
    back_button.image = back_image
    back_button.place(x=66, y=81)

    return canvas
