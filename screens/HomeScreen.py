import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from misc.utility import ApplicationState

# from screens import SettingsScreen
from screens import LoginScreen


def HomeScreen(window: tk.Tk, application_state: ApplicationState):
    # Homescreen setup code...
    hero_image = Image.open("./assets/recycle.png")
    settings = Image.open("./assets/settings.png")

    # Images
    recycle_image = ImageTk.PhotoImage(hero_image)
    settings_image = ImageTk.PhotoImage(settings)

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
        270.0,
        70.0,
        anchor="nw",
        text="Welcome",
        fill="#000000",
        font=("Kadwa Bold", 40),
    )

    canvas.create_text(
        200.0,
        130.0,
        anchor="nw",
        text="To the Bottle Collection System",
        fill="#000000",
        font=("Kadwa Regular", 20),
    )
    canvas.create_text(
        323.0,
        249.0,
        anchor="nw",
        text="Please insert a recyclable bottle to start ...",
        fill="#515050",
        font=("Kadwa Regular", 15),
    )
    canvas.create_image(117, 203, anchor=tk.NW, image=recycle_image)
    canvas.recycle_image = recycle_image

    # Settings button
    settings_button = tk.Label(
        window,
        image=settings_image,
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )

    settings_button.image = settings_image
    settings_button.bind(
        "<Button-1>",
        # lambda _: SettingsScreen.SettingsScreen(window, application_state),
        lambda _: LoginScreen.LoginScreen(window, application_state),
    )
    settings_button.place(x=561, y=393)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
