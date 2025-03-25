import tkinter as tk
from tkinter import ttk

class CommoditySelection:
    def __init__(self, root, update_units_callback, unit_conversions):
        """
        Initialize the CommoditySelection class.

        Args:
            root (tk.Tk): The root window or frame where the commodity selection will be placed.
            update_units_callback (function): Callback function to update the unit dropdown based on the selected commodity.
            unit_conversions (dict): A dictionary containing unit conversions for each commodity.
        """
        self.root = root
        self.update_units_callback = update_units_callback
        self.UNIT_CONVERSIONS = unit_conversions

        # Create the main frame for the CommoditySelection FIRST
        self.frame = ttk.Frame(root, style="White.TFrame")  # Must be created first
        self.frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Commodity Selection
        self.commodity_label = ttk.Label(self.frame, text="Commodity:", style="White.TLabel")
        self.commodity_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.commodity_var = tk.StringVar(value="soybeans")
        self.commodity_dropdown = ttk.Combobox(
            self.frame,
            textvariable=self.commodity_var,
            values=["soybeans", "sugar", "maize", "soybean_oil"],
            width=7
        )
        self.commodity_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Unit Selection
        self.unit_label = ttk.Label(self.frame, text="Unit:", style="White.TLabel")
        self.unit_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.unit_var = tk.StringVar(value="tonnes")
        self.unit_dropdown = ttk.Combobox(self.frame, textvariable=self.unit_var, width=7)
        self.unit_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Quantity Field - Added below unit selection
        self.quantity_label = ttk.Label(self.frame, text="Quantity:", style="White.TLabel")
        self.quantity_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(
            self.frame,
            width=8,
            validate="key",
            validatecommand=(root.register(self.validate_quantity), "%P")
        )
        self.quantity_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Bind the function to the commodity dropdown
        self.commodity_dropdown.bind("<<ComboboxSelected>>", self.update_units)

        # Initialize the unit dropdown with the default commodity
        self.update_units()

    def validate_quantity(self, value):
        """Validate quantity input (positive numbers only)"""
        if value == "":
            return True
        try:
            return float(value) > 0
        except ValueError:
            return False

    def get_quantity(self):
        """Get the quantity value with validation"""
        try:
            return float(self.quantity_entry.get())
        except ValueError:
            return 0.0

    def update_units(self, event=None):
        """
        Update the unit dropdown options based on the selected commodity.
        """
        selected_commodity = self.commodity_var.get()
        if selected_commodity in self.UNIT_CONVERSIONS:
            units = list(self.UNIT_CONVERSIONS[selected_commodity].keys())
            self.unit_dropdown['values'] = units
            self.unit_var.set(units[0])  # Set the default unit
        else:
            self.unit_dropdown['values'] = []
            self.unit_var.set("")