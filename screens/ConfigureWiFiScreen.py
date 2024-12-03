import tkinter as tk
from tkinter import Canvas, ttk
from typing import List
from PIL import Image, ImageTk
from components.date_time import Add_date_time
from components.name_logo import Add_Name_Logo
from components.wifi_status import Add_Wifi_Status
from screens import SettingsScreen, WiFiConnectScreen
import threading

from misc.utility import ApplicationState, list_available_wifi


is_disabled = False  # Fix: Boolean are not threadsafe, encapsulate in class


# This function updates the Listbox in the main thread
def insert_into_listbox(
    wifi_listbox: tk.Listbox, available_networks: List[str], window: tk.Tk
):

    def update_listbox(wifi_listbox: tk.Listbox, available_networks: List[str]):
        wifi_listbox.delete(0, tk.END)  # Clear the listbox
        if not available_networks:
            wifi_listbox.insert(tk.END, "No Wi-Fi networks found.")
        else:
            for network in available_networks:
                wifi_listbox.insert(tk.END, network)

    # Schedule the update to happen in the main thread
    window.after(
        100,
        update_listbox,
        wifi_listbox,
        available_networks,
    )


def on_wifi_selected(
    _,
    listbox: tk.Listbox,
    window: tk.Tk,
    application_state: ApplicationState,
):
    # Get the index of the clicked item
    selected_index: int = int(listbox.curselection())  # type: ignore

    if selected_index:
        # Get the item at the selected index
        selected_item: str = str(listbox.get(selected_index))  # type: ignore
        WiFiConnectScreen.WiFiConnectScreen(window, application_state, selected_item)


# This function shows the loading indicator while fetching the Wi-Fi networks
def show_loading_indicator(canvas: Canvas, window: tk.Tk, wifi_listbox: tk.Listbox):
    global is_disabled
    # Create and place a loading indicator (progress bar)
    loading_text = ttk.Progressbar(
        window, orient="horizontal", mode="indeterminate", length=280
    )
    loading_text.place(x=260, y=240)  # Place it on the canvas
    loading_text.start()  # Start the progress bar animation
    canvas.update()

    # Disable all user interactions except for the progress bar
    is_disabled = True
    wifi_listbox.config(state="disabled")

    return loading_text


# This function hides the loading indicator once Wi-Fi networks are loaded
def hide_loading_indicator(
    loading_text: ttk.Progressbar, window: tk.Tk, wifi_listbox: tk.Listbox
):
    global is_disabled
    # Stop the progress bar animation and hide it
    loading_text.stop()
    loading_text.place_forget()  # Remove the progress bar from the window

    # Re-enable all user interactions
    is_disabled = False
    wifi_listbox.config(state="normal")


# This function handles the Wi-Fi list reload when the refresh button is clicked
def reload_button_handler(wifi_listbox: tk.Listbox, canvas: tk.Canvas, window: tk.Tk):
    if is_disabled:
        return

    loading_text = show_loading_indicator(canvas, window, wifi_listbox)

    # Load Wi-Fi networks in a separate thread
    def load_wifi_networks():
        try:
            available_networks = list_available_wifi(
                True
            )  # Fetch the available Wi-Fi networks
            # Once the networks are fetched, update the listbox
            window.after(
                0, insert_into_listbox, wifi_listbox, available_networks, window
            )
        finally:
            hide_loading_indicator(
                loading_text, window, wifi_listbox
            )  # Always hide the loading indicator

    # Start the loading in a separate thread
    threading.Thread(target=load_wifi_networks, daemon=True).start()


# This function is responsible for creating the Wi-Fi screen with the canvas, listbox, and buttons
def ConfigureWIFIScreen(window: tk.Tk, application_state: ApplicationState):
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
        250.0,
        70.0,
        anchor="nw",
        text="Select a Wi-Fi network",
        fill="#515050",
        font=("Kadwa Regular", 20),
    )

    # Back button to go to Settings screen
    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Label(
        window,
        image=back_image,  # type: ignore
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
    back_button.image = back_image  # type: ignore as we are doing this to keep reference to image
    back_button.place(x=66, y=81)

    # Create a listbox to display the networks
    wifi_listbox = tk.Listbox(
        window, font=("Kadwa Regular", 18), width=50, height=10, selectmode=tk.SINGLE
    )

    # Refresh Button
    refresh_image = ImageTk.PhotoImage(refresh)
    refresh_button = tk.Label(
        window,
        image=refresh_image,  # type: ignore
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        padx=10,
        pady=10,
    )
    refresh_button.bind(
        "<Button-1>",
        lambda _: reload_button_handler(wifi_listbox, canvas, window),
    )
    refresh_button.image = refresh_image  # type: ignore as we are doing this to keep reference to image
    refresh_button.place(x=700, y=81)

    # Load initial Wi-Fi networks
    insert_into_listbox(wifi_listbox, list_available_wifi(False), window)

    wifi_listbox.bind(
        "<ButtonRelease-1>",
        lambda event: on_wifi_selected(
            event,
            wifi_listbox,
            window,
            application_state,
        ),
    )
    wifi_listbox.place(x=80, y=150)

    # Function for displaying name and logo
    Add_Name_Logo(canvas)

    # Function for displaying date and time
    Add_date_time(window)

    # Function for displaying Wi-Fi status
    Add_Wifi_Status(canvas, application_state)

    return canvas
