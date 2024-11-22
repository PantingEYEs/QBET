"""
File name:
  selection_tool.py

Function:
  Provides pixel selection and cropping tools for images, handles the cropping of selected areas.

Dependencies:
  tkinter
  PIL
  
"""


# celection_tool.py

import tkinter as tk
from PIL import Image, ImageTk # type: ignore

class SelectionTool(tk.Frame):
    def __init__(self, parent, image_path, callback):
        super().__init__(parent)
        self.image_path = image_path
        self.callback = callback
        self.selected_areas = []  # Store selected areas
        self.start_x = self.start_y = 0
        self.rect = None
        self.load_image()  # Load and scale image
        self.setup_tool()  # Initialize selection tool components

    def load_image(self):
        original_image = Image.open(self.image_path)
        width, height = original_image.size
        new_height = 500  # Set height limit

        if height > new_height:
            scale_factor = new_height / height
            new_width = int(width * scale_factor)
            new_height = new_height
        else:
            new_width, new_height = width, height

        self.image = original_image.resize((new_width, new_height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

    def setup_tool(self):
        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        # Bind mouse events for selection
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        self.select_button = tk.Button(self, text="Select answers", command=self.on_select_answers)
        self.select_button.pack(pady=10)
        self.select_button.pack_forget()  # Initially hidden

        # Bind Ctrl+Z for undo
        self.master.bind("<Control-z>", self.undo_selection)

    def start_selection(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def update_selection(self, event):
        cur_x, cur_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline="red")

    def end_selection(self, event):
        end_x, end_y = event.x, event.y
        selected_area = (self.start_x, self.start_y, end_x, end_y)
        self.selected_areas.append(selected_area)
        self.redraw_canvas()  # Show the selected area on canvas
        self.select_button.pack()

    def undo_selection(self, event=None):
        if self.selected_areas:
            self.selected_areas.pop()
            self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
        for area in self.selected_areas:
            self.canvas.create_rectangle(area, outline="red", width=2)
        self.select_button.pack() if self.selected_areas else self.select_button.pack_forget()

    def on_select_answers(self):
        if self.selected_areas:
            print(f"Selected areas: {self.selected_areas}")
            self.callback(self.selected_areas)
