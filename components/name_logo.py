import tkinter as tk


def Add_Name_Logo(canvas: tk.Canvas):
    canvas.create_text(
        300.0,
        19.0,
        anchor="nw",
        text="Re-Bottle",
        fill="#000000",
        font=("Kadwa Bold", 30),
    )
