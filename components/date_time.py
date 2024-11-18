import tkinter as tk
from time import strftime


def Add_date_time(window: tk.Tk):
    time_display = tk.Label(
        window,
        text="",
        font=("Kadwa Regular", 10),
        fg="#515050",
        bg="#FFFFFF",
    )
    time_display.place(x=20, y=10)

    # Date label for displaying current date
    date_display = tk.Label(
        window,
        text="",
        font=("Kadwa Regular", 10),
        fg="#515050",
        bg="#FFFFFF",
    )
    date_display.place(x=60, y=10)

    def time():
        # Get current date and time
        time_display.config(text=strftime("%H:%M"))
        date_display.config(text=strftime("%d/%m/%Y"))

        # Call time function every 1000ms (1 second)
        time_display.after(1000, time)

    # Start the time function to update the time
    time()
