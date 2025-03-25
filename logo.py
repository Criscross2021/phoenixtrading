import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Logo:
    def __init__(self, root, logo_path):
        self.root = root
        self.logo_path = logo_path
        self.logo_photo = None
        self.logo_label = None

    def load_logo(self):
        """Load and display the logo with proper sizing and no borders"""
        try:
            # Load and resize logo with exact dimensions
            logo_image = Image.open(self.logo_path).convert("RGBA")
            logo_image = logo_image.resize((43, 43), Image.Resampling.LANCZOS)

            # Create transparent background
            transparent_image = Image.new("RGBA", logo_image.size, (0, 0, 0, 0))
            transparent_image.paste(logo_image, (0, 0), logo_image)

            # Convert to PhotoImage - this already contains the size information
            self.logo_photo = ImageTk.PhotoImage(transparent_image)

            # Create the label - let the image determine the size
            self.logo_label = ttk.Label(
                self.root,
                image=self.logo_photo,
                style="Transparent.TLabel",
                padding=0  # Remove any default padding
            )
            self.logo_label.image = self.logo_photo  # Keep reference

            return self.logo_label

        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback - simple text label with approximate size
            self.logo_label = ttk.Label(
                self.root,
                text="Logo",
                style="Transparent.TLabel",
                width=6,  # Width in characters
                padding=0
            )
            return self.logo_label