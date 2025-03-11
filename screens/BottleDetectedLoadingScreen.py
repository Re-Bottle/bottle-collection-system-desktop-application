from datetime import datetime
import tkinter as tk
from tkinter import Canvas, ttk

from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status

# from interface.custom_data_send import publish_mqtt
from interface.server_communicate import createScan
from misc.utility import BOTTLE_TYPE, ApplicationState, get_device_id
from screens import FinalScreen


def BottleDetectedLoadingScreen(window: tk.Tk, application_state: ApplicationState):

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
        250.0,
        70.0,
        anchor="nw",
        text="Bottle detected, please wait...",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

    progress_bar = ttk.Progressbar(
        window,
        orient="horizontal",
        length=200,
        mode="indeterminate",
    )

    progress_bar.place(x=300, y=250)
    progress_bar.start()

    # TODO: uncomment below code and on_send_data() call
    # def on_send_data():
    #     publish_mqtt(get_device_id())

    def load_final_screen():
        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        progress_bar.stop()  # Stop the progress bar animation
        # run the bottle detection function..........
        # on_send_data()
        scanData = f"{get_device_id()}{timestamp_str}"
        print(scanData)

        createScan(
            device_id=get_device_id(),
            scan_data=scanData,
            bottle_type=BOTTLE_TYPE.LITRE1.value,
        )
        FinalScreen.FinalScreen(
            window, application_state, scanData
        )  # Go to next screen

    window.after(5000, load_final_screen)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
