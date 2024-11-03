"""
File name:
  browse_handler.py

Function:
  Handles folder/file browsing functionality, file path display, and updates selected path.

Dependencies:
  tkinter

"""


# browse_handler.py

from tkinter import filedialog
from tkinter import messagebox

class BrowseHandler:
    def __init__(self, parent_label, update_source_path):
        self.parent_label = parent_label
        self.update_source_path = update_source_path 

    def open_file_dialog(self):
        # Open a dialog to choose either a directory or a file
        selected_path = filedialog.askdirectory()
        if not selected_path:
            selected_path = filedialog.askopenfilename()
        # Update the label and call the callback to update path in image_processor
        if selected_path:
            self.parent_label.config(text=selected_path)
            self.update_source_path(selected_path)
            print(f"Selected path: {selected_path}")  # Debug statement
        else:
            messagebox.showinfo(title="No path selected", message="Please choose a valid file or folder.") 
