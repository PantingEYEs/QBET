"""
File name:
  main.py

Function:
  Main entry file;
  Initializes the GUI and handles transitions between interfaces.

Dependencies:
  glob
  threading
  tkinter

"""


import glob
import threading
import tkinter as tk
from tkinter import messagebox
from gui_interface import Interface1, Interface2, Interface3
from file_validator import validate_setup
from image_processor import process_images

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
        """Destroy the current frame if it exists."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None  # Reset current frame reference

    def show_interface1(self): 
        """Display Interface1 and initialize the image processing callback."""
        self.clear_current_frame()
        self.current_frame = Interface1(self.root, self.init_image_processing)
        self.current_frame.pack(fill="both", expand=True)

    def init_image_processing(self, selected_path):
        """Start the image processing in a new thread and update UI."""
        self.current_frame.display_initializing()  # Show initializing text in Interface1
        self.root.update_idletasks()  # Force update to show initializing text
        print(f"Selected path for processing: {selected_path}")
        processing_thread = threading.Thread(target=self.process_images_wrapper, args=(selected_path,))  # Start a thread for processing images to keep UI responsive
        processing_thread.start()

    def process_images_wrapper(self, selected_path):
        """Wrapper function for image processing."""
        try:
            last_img_serial_num = process_images(selected_path)
            self.root.after(100, self.finalize_processing, last_img_serial_num)
        except Exception as e:
            print(f"Error during image processing: {e}")
            self.root.after(100, self.handle_processing_error)

    def finalize_processing(self, last_img_serial_num):
        """Finalize image processing and display a completion message."""
        if last_img_serial_num is not None:
            msg = f"The last serial number={last_img_serial_num} variable declaration succeeded, {last_img_serial_num} images have been selected."
        else:
            msg = "Image processing completed with no images selected."
        if messagebox.showinfo("Processing Complete", msg):
            # Use glob with a more concise way to gather images
            image_files = glob.glob("input/*.[jp][np]g") + glob.glob("input/*.png") + glob.glob("input/*.heic") + glob.glob("input/*.gif")
            if image_files:
                self.show_interface2(image_files[0])
            else:
                messagebox.showerror("Error", "No images found in the input folder.")
    def show_interface2(self, image_path):
        """Display Interface2 for image cropping."""
        self.clear_current_frame()
        self.current_frame = Interface2(self.root, image_path, self.show_interface3, self.show_interface1, self.on_selection_made)
        self.current_frame.pack(fill="both", expand=True)

    def on_selection_made(self, selected_area):
        """Handle the selected area from Interface2."""
        # 处理选择的区域，可能包括进一步的处理或传递给 Interface3
        print(f"Selected area: {selected_area}")
        # 在这里可以选择进入 Interface3 或进行其他操作

    def show_interface3(self):
        """Display Interface3 for the final stage of processing."""
        self.clear_current_frame()
        self.current_frame = Interface3(self.root, self.show_interface2)
        self.current_frame.pack(fill="both", expand=True)

    def handle_processing_error(self):
        """Handle errors during image processing and restore UI state.""" 
        messagebox.showerror("Error", "An error occurred during image processing.")
        self.show_interface1()  # Return to the first interface for user to retry

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
