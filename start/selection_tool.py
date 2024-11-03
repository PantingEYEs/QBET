"""
File name:
  selection_tool.py

Function:
  Provides pixel selection and cropping tools for images, handles the cropping of selected areas.

Dependencies:
  os
  PIL


import os
from PIL import Image, ImageDraw, ImageTk

class SelectionTool:
    def __init__(self, image_path):
        if not os.path.exists(image_path) or image_path is None:
            raise ValueError(f"Invalid image path: {image_path}")
        
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.drawn_image = self.image.copy()
        self.draw = ImageDraw.Draw(self.drawn_image)
        self.selections = []

    def add_selection(self, selection):
        #Add a selection rectangle to the image.
        
        #Args:
        #    selection (tuple): A tuple of (left, upper, right, lower) representing the bounding box of the selection.
        
        if not self._is_selection_valid(selection):
            raise ValueError("Invalid selection coordinates.")
        
        self.selections.append(selection)
        self.draw.rectangle(selection, outline="red", width=2)

    def clear_selections(self):
        #Clear all selections.
        self.selections = []
        self.drawn_image = self.image.copy()

    def save_cropped_image(self, output_path):
        #Save a cropped image based on selections.
        
        #Args:
        #    output_path (str): The path where the cropped image will be saved.
        
        #Raises:
        #    ValueError: If there are no selections to crop.
        
        if not self.selections:
            raise ValueError("No selections to crop.")
        
        cropped_image = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
        
        for selection in self.selections:
            cropped_part = self.image.crop(selection)
            cropped_image.paste(cropped_part, selection)

        # Save the image in PNG format by default, but you can change the format if needed
        cropped_image.save(output_path, format="PNG")

    def get_tk_image(self):
        #Convert the drawn image to a format usable by Tkinter.

        #Returns:
        #    ImageTk.PhotoImage: A Tkinter-compatible image.
        
        #return ImageTk.PhotoImage(self.drawn_image)

    def _is_selection_valid(self, selection):
        #Check if the selection is valid (within image bounds).
        
        #Args:
        #    selection (tuple): The selection coordinates to check.
        
        #Returns:
        #    bool: True if the selection is valid, False otherwise.
        
        left, upper, right, lower = selection
        return (0 <= left < right <= self.image.width) and (0 <= upper < lower <= self.image.height)
    
      """