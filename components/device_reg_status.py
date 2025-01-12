import tkinter as tk
from PIL import Image, ImageTk

from misc.utility import ApplicationState, get_device_details


def Add_Device_Reg_Status(canvas: tk.Canvas, applicationState: ApplicationState):
    registration_successful = Image.open(
        "./assets/registered.png"
    )  # Image when registration is successful
    registration_failed = Image.open(
        "./assets/not_registered.png"
    )  # Image when registration fails

    # Convert images to PhotoImage objects
    successful_image = ImageTk.PhotoImage(registration_successful)
    failed_image = ImageTk.PhotoImage(registration_failed)

    # Add text to indicate status
    canvas.create_text(
        580.0,
        15.0,
        anchor="nw",
        text=get_device_details().value,
        fill="#515050",
        font=("Kadwa Regular", 10),
    )

    canvas.create_image(  # type: ignore
        550,
        10,
        anchor=tk.NW,
        image=(
            successful_image
            if get_device_details().value == "Registered"
            else failed_image
        ),
    )
    

    canvas.image_success = successful_image  # type: ignore as we are doing this to keep reference to image
    canvas.image_failed = failed_image  # type: ignore as we are doing this to keep reference to image
