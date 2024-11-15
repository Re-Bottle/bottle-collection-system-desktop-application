import tkinter as tk
from screens import HomeScreen


def on_escape(event=None):
    window.quit()


# Main Window
window = tk.Tk()
window.overrideredirect(True)
window.geometry("800x480")
window.configure(bg="#FFFFFF")
window.title("Bottle Collection System")
window.bind("<Escape>", on_escape)

HomeScreenCanvas = HomeScreen.HomeScreen(window)


window.mainloop()
