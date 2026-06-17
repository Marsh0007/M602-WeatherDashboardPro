import tkinter as tk
from theme import BUTTON_FONT


class RoundedButton(tk.Canvas):

    def __init__(self, parent, text, command, bg_color, hover_color, width=220, height=42):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg"],
            highlightthickness=0
        )

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color

        self.button = self.create_round_rect(
            2, 2, width - 2, height - 2, 18,
            fill=bg_color,
            outline=""
        )

        self.create_text(
            width / 2,
            height / 2,
            text=text,
            fill="white",
            font=BUTTON_FONT
        )

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        self.command()

    def on_enter(self, event):
        self.itemconfig(self.button, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.button, fill=self.bg_color)