import tkinter as tk
from tkinter import Canvas, messagebox, ttk
from PIL import Image, ImageTk
import qrcode

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from main import WIFI_STATE

from screens import HomeScreen


def generate_qr_on_canvas(canvas, text):
    """
    Generates a QR code from the provided text and displays it on the given Tkinter Canvas.

    Parameters:
    - canvas: The Tkinter Canvas widget where the QR code will be displayed.
    - text: The text to be encoded into the QR code.
    """
    if not text:
        print("Error: No text provided for QR code.")
        return

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,  # QR code size (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Size of each box in the QR code
        border=4,  # Border thickness
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill="black", back_color="white")

    # Convert the image to a format Tkinter can display
    img_tk = ImageTk.PhotoImage(img)

    # Display the image on the canvas
    canvas.create_image(450, 80, image=img_tk, anchor="nw")

    # Keep a reference to the image to avoid garbage collection
    canvas.img_tk = img_tk  # Save the image reference in the canvas


def FinalScreen(window: tk.Tk, application_state: dict, qrCode: str):
    back_to_home = Image.open("./assets/back_to_home.png")

    back_to_home_image = ImageTk.PhotoImage(back_to_home)

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
        300.0,
        70.0,
        anchor="nw",
        text="Thank you!",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

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

    canvas.create_text(
        450.0,
        400.0,
        anchor="nw",
        text="Scan to verify your reward.",
        fill="#000000",
        font=("Kadwa Regular", 15),
    )

    generate_qr_on_canvas(canvas, qrCode)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
