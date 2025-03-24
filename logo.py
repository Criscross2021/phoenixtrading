import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Logo:
    def __init__(self, root, logo_path):
        """
        Initialize the Logo class.

        Args:
            root (tk.Tk): The root window or frame where the logo will be displayed.
            logo_path (str): The path to the logo image file.
        """
        self.root = root
        self.logo_path = logo_path
        self.logo_photo = None
        self.logo_label = None

    def load_logo(self):
        """
        Load and display the logo in the GUI.

        Returns:
            ttk.Label: The label containing the logo.
        """
        try:
            # Load the logo image with transparency
            logo_image = Image.open(self.logo_path).convert("RGBA")  # Ensure the image has an alpha channel
            logo_image = logo_image.resize((43, 43), Image.Resampling.LANCZOS)

            # Create a transparent background image
            transparent_image = Image.new("RGBA", logo_image.size, (0, 0, 0, 0))
            transparent_image.paste(logo_image, (0, 0), logo_image)  # Paste the logo with its alpha channel

            # Convert the transparent image to a PhotoImage
            self.logo_photo = ImageTk.PhotoImage(transparent_image)

            # Create a label to display the logo with a transparent background
            self.logo_label = ttk.Label(self.root, image=self.logo_photo, style="Transparent.TLabel")
            self.logo_label.image = self.logo_photo  # Keep a reference to avoid garbage collection
            return self.logo_label

        except Exception as e:
            # Handle errors (e.g., file not found or invalid image)
            print(f"Error loading logo: {e}")
            self.logo_label = ttk.Label(self.root, text="Logo not found", style="Transparent.TLabel")
            return self.logo_label