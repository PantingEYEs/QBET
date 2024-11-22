"""
File name:
  main.py

Function:
  Main entry file; initializes the GUI and handles transitions between interfaces.

Dependencies:
  glob
  threading
  tkinter

"""


# main.py

import glob
import threading
import tkinter as tk
from tkinter import messagebox
from file_validator import validate_setup
from image_processor import process_images
from browse_handler import BrowseHandler
from selection_tool import SelectionTool
from gui_interface import Interface1, Interface2, Interface3

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QBET v1.0")
        self.root.geometry("800x600")
        if not validate_setup():
            messagebox.showerror("Error", "Some dependencies are missing.")
            print("Missing dependencies detected. Exiting application.")
            self.root.quit()
        self.current_frame = None
        self.show_interface1()

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_interface1(self):
        self.clear_current_frame()
        self.current_frame = Interface1(self.root, self.init_image_processing)
        self.current_frame.pack(fill="both", expand=True)

    def init_image_processing(self, selected_path):
        self.current_frame.display_initializing()
        self.root.update_idletasks()
        print(f"Selected path for processing: {selected_path}")
        processing_thread = threading.Thread(target=self.process_images_wrapper, args=(selected_path,))
        processing_thread.start()

    def process_images_wrapper(self, selected_path):
        try:
            last_img_serial_num = process_images(selected_path)
            self.root.after(100, self.finalize_processing, last_img_serial_num)
        except Exception as e:
            print(f"Error during image processing: {e}")
            self.root.after(100, self.handle_processing_error)

    def finalize_processing(self, last_img_serial_num):
        if last_img_serial_num is not None:
            msg = f"The last serial number={last_img_serial_num} variable declaration succeeded, {last_img_serial_num} images have been selected."
        else:
            msg = "Image processing completed with no images selected."
        if messagebox.showinfo("Processing Complete", msg):
            image_files = glob.glob("input/*.[jp][np]g") + glob.glob("input/*.png") + glob.glob("input/*.heic") + glob.glob("input/*.gif")
            if image_files:
                self.show_interface2(image_files[0])
            else:
                messagebox.showerror("Error", "No images found in the input folder.")

    def show_interface2(self, image_path):
        self.clear_current_frame()
        self.current_frame = Interface2(self.root, image_path, self.on_selection_made)
        self.current_frame.pack(fill="both", expand=True)

    def on_selection_made(self, selected_areas):
        print(f"Selected areas: {selected_areas}")

    def handle_processing_error(self):
        messagebox.showerror("Error", "An error occurred during image processing.")
        self.show_interface1()

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
        self.dot_count = 0

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
        self.dot_count = (self.dot_count + 1) % 7
        dots = '.' * self.dot_count
        self.status_label.config(text=f"Initializing{dots}")
        self.after(500, self.update_text_animation)

    def display_initializing(self):
        for widget in self.winfo_children():
            widget.destroy()
    
        self.dot_count = 0
        self.status_label = tk.Label(self, text="Initializing")
        self.status_label.pack(pady=10)
        self.update_text_animation()

    def show_next_button(self, num_images):
        for widget in self.winfo_children():
            widget.destroy()
        self.status_label = tk.Label(self, text=f"{num_images} images selected.")
        self.status_label.pack(pady=10)
        self.next_button = tk.Button(self, text="Next", command=self.on_next_interface)
        self.next_button.pack(pady=10)

    def on_next_interface(self):
        self.start_processing_callback = None
        self.pack_forget()

class Interface2(tk.Frame):
    def __init__(self, root, image_path, selection_callback):
        super().__init__(root)
        self.selection_callback = selection_callback
        
        tk.Label(self, text="Select the area you want to crop.").pack(pady=10)

        self.selection_tool = SelectionTool(self, image_path, self.on_selection_made)
        self.selection_tool.pack(fill="both", expand=True)

    def on_selection_made(self, selected_areas):
        self.selection_callback(selected_areas)

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
        self.qb_content.config(state=tk.NORMAL)
        self.qb_content.delete('1.0', tk.END)
        self.qb_content.insert(tk.END, "Updated content from QB.md")
        self.qb_content.config(state=tk.DISABLED)

    def on_next(self):
        self.next_callback()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
