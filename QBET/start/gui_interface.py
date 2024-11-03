"""
File name:
  gui_interface.py

Function:
  Contains functions for building the GUI, defining buttons, and layout for each interface view.

Dependencies:
  tkinter, PIL
"""

# gui_interface.py

import tkinter as tk
from PIL import Image, ImageTk
from browse_handler import BrowseHandler

class Interface1(tk.Frame):
    def __init__(self, root, start_processing_callback):
        super().__init__(root)
        self.start_processing_callback = start_processing_callback
        self.processing_started = False
        self.selected_path = tk.StringVar()
        
        tk.Label(self, text="Please select a picture.").pack(pady=10)
        self.browse_button = tk.Button(self, text="Browse...", command=self.browse_file)
        self.browse_button.pack(pady=5)
        
        self.path_label = tk.Label(self, textvariable=self.selected_path)
        self.path_label.pack(pady=5)
        
        self.next_button = tk.Button(self, text="Next", command=self.on_next)
        self.next_button.pack(pady=10)
        self.next_button.config(state=tk.DISABLED)
        
        self.status_label = None
        self.dot_count = 0  # Counter for loading animation

    def browse_file(self):
        browse_handler = BrowseHandler(self.path_label, self.set_selected_path)
        browse_handler.open_file_dialog()

    def set_selected_path(self, path):
        self.selected_path.set(path)
        self.next_button.config(state=tk.NORMAL)

    def on_next(self):
        if not self.processing_started:
            self.processing_started = True
            self.start_processing_callback(self.selected_path.get())
            self.display_initializing()

    def update_text_animation(self):
        """Animate the 'Initializing' text with dots."""
        self.dot_count = (self.dot_count + 1) % 7  # Loop from 0 to 6
        dots = '.' * self.dot_count
        self.status_label.config(text=f"Initializing{dots}")
        self.after(500, self.update_text_animation)  # Update every 500ms

    def display_initializing(self):
        """Display the initializing state."""
        for widget in self.winfo_children():
            widget.destroy()
    
        self.dot_count = 0  # Reset counter
        self.status_label = tk.Label(self, text="Initializing")  # Initial text
        self.status_label.pack(pady=10)
        self.update_text_animation()  # Start the text animation

    def show_next_button(self, num_images):
        """Display the next button with the number of images selected."""
        for widget in self.winfo_children():
            widget.destroy()
        self.status_label = tk.Label(self, text=f"{num_images} images selected.")
        self.status_label.pack(pady=10)
        self.next_button = tk.Button(self, text="Next", command=self.on_next_interface)
        self.next_button.pack(pady=10)

    def on_next_interface(self):
        """Transition to the next interface."""
        self.start_processing_callback = None  # Disable callback to prevent re-triggering
        self.pack_forget()  # Hide this frame

class Interface2(tk.Frame):
    def __init__(self, root, image_path, next_callback, back_callback, selection_callback):
        super().__init__(root)
        self.next_callback = next_callback
        self.back_callback = back_callback
        self.selection_callback = selection_callback

        # Instruction label
        tk.Label(self, text="Select the area you want to crop.").pack(pady=10)

        # Load image and resize to keep aspect ratio
        original_image = Image.open(image_path)
        max_height = 500
        width, height = original_image.size

        # Calculate the new size while maintaining aspect ratio
        if height > max_height:
            scale_factor = max_height / height
            new_width = int(width * scale_factor)
            new_height = max_height
        else:
            new_width = width
            new_height = height

        # Resize the image using LANCZOS filter
        self.image = original_image.resize((new_width, new_height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self, width=new_width, height=new_height)
        self.canvas.pack()
        
        # Load image into the canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        # Mouse event bindings
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        # Initialize selection coordinates
        self.start_x = self.start_y = 0
        self.rect = None

        # Next and Back buttons
        self.next_button = tk.Button(self, text="Next", command=self.on_next)
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=10)
        self.back_button = tk.Button(self, text="Back", command=self.on_back)
        self.back_button.pack(side=tk.LEFT, padx=5, pady=10)
        
    def start_selection(self, event):
        """Start selection rectangle."""
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def update_selection(self, event):
        """Update selection rectangle as mouse moves."""
        cur_x, cur_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline="red")

    def end_selection(self, event):
        """Handle the end of selection. Save the selected area."""
        end_x, end_y = event.x, event.y
        selected_area = (self.start_x, self.start_y, end_x, end_y)  # Store selected area
        self.selection_callback(selected_area)  # Call selection callback

    def on_next(self):
        """Callback for next button."""
        self.next_callback()

    def on_back(self):
        """Callback for back button."""
        self.back_callback()

class Interface3(tk.Frame):
    def __init__(self, root, next_callback):
        super().__init__(root)
        self.next_callback = next_callback
        tk.Label(self, text="OCR Result Display: QB.md").pack(pady=10)
        self.qb_content = tk.Text(self, height=15, width=50, state=tk.DISABLED)
        self.qb_content.pack(pady=5)
        self.refresh_button = tk.Button(self, text="Refresh", command=self.refresh_content)
        self.refresh_button.pack(pady=5)
        self.next_button = tk.Button(self, text="Next", command=self.on_next)
        self.next_button.pack(pady=10)

    def refresh_content(self):
        """Refresh QB.md content display."""
        self.qb_content.config(state=tk.NORMAL)
        self.qb_content.delete("1.0", tk.END)
        
        try:
            with open("output/QB.md", "r") as file:
                self.qb_content.insert(tk.END, file.read())
        except FileNotFoundError:
            self.qb_content.insert(tk.END, "QB.md not found. Please check output directory.")
        
        self.qb_content.config(state=tk.DISABLED)

    def on_next(self):
        """Handle the Next button click to go back to Interface 2."""
        self.next_callback()
