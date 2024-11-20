import tkinter as tk


def Add_Keyboard(
    window: tk.Tk,
    passcode_var: tk.StringVar,
):
    # Virtual Keyboard buttons
    keyboard_buttons = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
        "o",
        "p",
        "a",
        "s",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "z",
        "x",
        "c",
        "v",
        "b",
        "n",
        "m",
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "_",
        "+",
        "-",
        "=",
        "[",
        "]",
        "{",
        "}",
        "|",
        ";",
        ":",
        "'",
        '"',
        ",",
        ".",
        "<",
        ">",
        "/",
        "?",
        "shift",
    ]

    shift_active = False  # Track shift state

    def on_button_click(char):
        # Check if shift is active and make the letter uppercase (alphabet characters only)
        if shift_active and char.isalpha():
            char = char.upper()
        current_text = passcode_var.get()
        if len(current_text) >= 6:
            return
        passcode_var.set(current_text + char)

    def toggle_shift():
        nonlocal shift_active
        shift_active = not shift_active
        shift_button.config(bg="#93B15A" if shift_active else "#FFFFFF")
        update_keyboard_text()

    def update_keyboard_text():
        """Update the text of alphabetic buttons based on the shift state."""
        for button in buttons:
            char = button.cget("text")
            if char.isalpha():  # Only update alphabetic characters
                new_text = char.upper() if shift_active else char.lower()
                button.config(text=new_text)

    row, col = 1, 0
    buttons = []  # Store references to all buttons

    for char in keyboard_buttons:
        if char != "shift":  # Only create button for characters, not for "shift"
            button = tk.Button(
                window,
                text=char,
                width=4,
                height=1,
                font=("Arial", 12),
                command=lambda char=char: on_button_click(char),
            )
            button.place(x=30 + col * 55, y=230 + row * 40)
            buttons.append(button)  # Store button reference
            col += 1
            if col > 13:  # New row after 13 buttons
                col = 0
                row += 1

    # Shift button to toggle between lower and upper case
    shift_button = tk.Button(
        window,
        text="Shift",
        width=4,
        height=1,
        font=("Arial", 12),
        command=toggle_shift,  # Toggle shift state when clicked
        bg="#FFFFFF",
    )
    shift_button.place(x=30 + col * 55, y=230 + row * 40)
    col += 1

    # backspace
    def backspace():
        current_passcode = passcode_var.get()  # Get the current passcode
        if len(current_passcode) > 0:
            # Remove the last character of the passcode
            new_passcode = current_passcode[:-1]
            passcode_var.set(new_passcode)

    backspace_button = tk.Button(
        window, text="←", width=4, height=1, font=("Arial", 12), command=backspace
    )
    backspace_button.place(x=30 + (col) * 55, y=230 + row * 40)

    # Clear button to reset passcode entry
    clear_button = tk.Button(
        window,
        text="Clear",
        width=4,
        height=1,
        font=("Arial", 12),
        command=lambda: passcode_var.set(""),
    )
    clear_button.place(x=30 + (col + 1) * 55, y=230 + row * 40)
