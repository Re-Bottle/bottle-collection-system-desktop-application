import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk

# import boto3
# import os

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from screens import SettingsScreen

from misc.utility import ApplicationState, list_available_wifi
from main import WIFI_STATE

uniqueID = "1234567890"
is_disabled = False
# # Initialize IoT client
# client = boto3.client(
#     "iot",
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#     region_name="ap-south-1",
# )


# def create_provisioning_claim():
#     # Create keys and certificate (this is often part of the provisioning claim)
#     response = client.create_keys_and_certificate(setAsActive=True)
#     # response = client.create_provisioning_claim(templateName="default", certificateId=response["certificateId"])

#     print("Provisioning Claim Created:")
#     print("Certificate ARN:", response["certificateArn"])
#     print("Certificate PEM:", response["certificatePem"])
#     print("Certificate ID:", response["certificateId"])
#     print("Key Pair:")
#     print("Private Key:", response["keyPair"]["PrivateKey"])
#     print("Public Key:", response["keyPair"]["PublicKey"])

#     return response


# create_provisioning_claim()


# This function handles to the reload and check if device is registered when the refresh button is clicked
def refresh_button_handler(canvas, window):

    return


def RegisterDeviceScreen(window: tk.Tk, application_state: ApplicationState):
    refresh = Image.open("./assets/reload.png")
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
        210.0,
        240.0,
        anchor="nw",
        text="Unique ID for your device is:",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

    canvas.create_text(
        300.0,
        290.0,
        anchor="nw",
        text=uniqueID,
        fill="#93B15A",
        font=("Kadwa Regular", 20),
    )

    # Back button to go to Settings screen
    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Label(
        window,
        image=back_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    back_button.bind(
        "<Button-1>",
        lambda _: (
            SettingsScreen.SettingsScreen(window, application_state)
            if not is_disabled
            else None
        ),
    )
    back_button.image = back_image
    back_button.place(x=66, y=81)

    # Refresh Button
    refresh_image = ImageTk.PhotoImage(refresh)
    refresh_button = tk.Label(
        window,
        image=refresh_image,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    refresh_button.bind(
        "<Button-1>",
        lambda _: refresh_button_handler(canvas, window),
    )
    refresh_button.image = refresh_image
    refresh_button.place(x=700, y=81)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
