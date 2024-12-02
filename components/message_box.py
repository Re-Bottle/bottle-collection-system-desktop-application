import tkinter as tk


def show_custom_error(title, message, x=300, y=300):
    """Custom error messagebox at a specific position."""
    top = tk.Toplevel()
    top.title(title)
    top.geometry(f"+{x}+{y}")
    top.resizable(False, False)

    # Error icon
    label = tk.Label(top, text="❌", font=("Arial", 20), fg="red")
    label.pack(pady=(10, 5))

    # Error message
    message_label = tk.Label(top, text=message, font=("Arial", 12), wraplength=250)
    message_label.pack(pady=(0, 10))

    # OK button to close
    button = tk.Button(top, text="OK", command=top.destroy, bg="red", fg="white")
    button.pack(pady=(5, 10))

    # Ensure the window is displayed before setting the grab
    top.deiconify()  # Ensure it's visible
    top.update()  # Make sure it's fully initialized

    top.transient()  # Set as a dialog
    top.grab_set()  # Prevent interaction with other windows

    # Wait for the window to be closed before continuing
    top.wait_window(top)


def show_custom_info(title, message, x=300, y=300):
    """Custom info messagebox at a specific position."""
    top = tk.Toplevel()
    top.title(title)
    top.geometry(f"+{x}+{y}")
    top.resizable(False, False)

    # Info icon
    label = tk.Label(top, text="ℹ️", font=("Arial", 20), fg="blue")
    label.pack(pady=(10, 5))

    # Info message
    message_label = tk.Label(top, text=message, font=("Arial", 12), wraplength=250)
    message_label.pack(pady=(0, 10))

    # OK button to close
    button = tk.Button(top, text="OK", command=top.destroy, bg="blue", fg="white")
    button.pack(pady=(5, 10))

    # Ensure the window is displayed before setting the grab
    top.deiconify()  # Ensure it's visible
    top.update()  # Make sure it's fully initialized

    top.transient()  # Set as a dialog
    top.grab_set()  # Prevent interaction with other windows

    # Wait for the window to be closed before continuing
    top.wait_window(top)
