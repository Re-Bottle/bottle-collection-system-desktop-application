import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
from screens import SettingsScreen
import threading

from utility import list_available_wifi


def show_loading_indicator(canvas: Canvas, window: tk.Tk):
    # Create a loading indicator (simple text or an animated spinner)
    loading_text = canvas.create_text(
        400,
        240,
        anchor="center",
        text="Loading...",
        fill="#000000",
        font=("Kadwa Bold", 40 * -1),
    )
    canvas.update()

    # Disable all user interactions
    for widget in window.winfo_children():
        widget.config(state="disabled")

    return loading_text


def hide_loading_indicator(canvas: Canvas, loading_text, window: tk.Tk):
    # Remove loading text and re-enable all user interactions
    canvas.delete(loading_text)

    # Re-enable all user interactions
    for widget in window.winfo_children():
        widget.config(state="normal")


def insert_into_listbox(wifi_listbox: tk.Listbox, available_networks: list):
    wifi_listbox.delete(0, tk.END)
    if not available_networks:
        wifi_listbox.insert(tk.END, "No Wi-Fi networks found.")
        return
    for network in available_networks:
        wifi_listbox.insert(tk.END, network)


def on_wifi_selected(event, listbox: tk.Listbox):
    # Get the index of the clicked item
    selected_index: int = listbox.curselection()

    if selected_index:
        # Get the item at the selected index
        selected_item = listbox.get(selected_index)
        # Trigger an action based on the selected item (e.g., show a message)
        messagebox.showinfo("Item Clicked", f"You clicked: {selected_item}")


def reload_button_handler(wifi_listbox, canvas, window):
    loading_text = show_loading_indicator(canvas, window)
    insert_into_listbox(wifi_listbox, list_available_wifi(True))
    hide_loading_indicator(canvas, loading_text, window)


def configureWIFIScreen(window: tk.Tk, application_state: dict):
    wifi_connected = Image.open("./assets/connected.png")
    wifi_disconnected = Image.open("./assets/not-connected.png")
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

    # Load Wi-Fi connection images
    connected_image = ImageTk.PhotoImage(wifi_connected)
    not_connected_image = ImageTk.PhotoImage(wifi_disconnected)

    # Display the connection status (connected image)
    canvas.create_image(692, 10, anchor=tk.NW, image=connected_image)

    canvas.image2 = connected_image
    canvas.image3 = not_connected_image

    # Back button to go to Settings screen
    back_image = ImageTk.PhotoImage(back)
    back_button = tk.Label(
        window,
        image=back_image,
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )
    back_button.bind(
        "<Button-1>",
        lambda _: SettingsScreen.SettingsScreen(window, application_state),
    )
    back_button.image = back_image
    back_button.place(x=66, y=81)

    # Create a listbox to display the networks
    wifi_listbox = tk.Listbox(
        window, font=("Kadwa Regular", 18), width=50, height=10, selectmode=tk.SINGLE
    )

    # Refresh Button
    refresh_image = ImageTk.PhotoImage(refresh)
    refresh_button = tk.Label(
        window,
        image=refresh_image,
        borderwidth=0,  # Remove the border
        highlightthickness=0,  # Remove the highlight border
        relief="flat",  # Set the button relief to "flat" to avoid any raised or sunken borders
        bg="#FFFFFF",  # Set the background color to the same as the window
        padx=10,  # Add horizontal padding (space around the image)
        pady=10,  # Add vertical padding (space around the image)
    )
    refresh_button.bind(
        "<Button-1>",
        lambda _: threading.Thread(
            target=reload_button_handler,
            args=(wifi_listbox, canvas, window),
            daemon=True,
        ).start(),
    )
    refresh_button.image = refresh_image
    refresh_button.place(x=700, y=81)

    insert_into_listbox(wifi_listbox, list_available_wifi(False))

    wifi_listbox.bind(
        "<ButtonRelease-1>", lambda event: on_wifi_selected(event, wifi_listbox)
    )
    wifi_listbox.place(x=80, y=150)
    return canvas
