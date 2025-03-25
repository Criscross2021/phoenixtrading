import tkinter as tk
from tkinter import ttk

class AdditionalCostsFrame(ttk.Frame):
    def __init__(self, parent, validate_input_func):
        super().__init__(parent, style="White.TFrame")
        """
        Initialize the AdditionalCostsFrame.

        Args:
            parent: The parent widget (usually a notebook tab).
            validate_input_func: Function to validate input in the cost fields.
        """
        self.validate_input_func = validate_input_func
        self.cost_entries = {}

        # Create input fields for additional costs
        self.create_additional_costs_fields()

    def create_additional_costs_fields(self):
        """Create input fields for additional costs."""
        # Profit Sharing
        profit_sharing_label = ttk.Label(
            self,
            text="Profit Sharing (USD/MT):",
            style="AdditionalCosts.TLabel"  # Use our new consistent style
        )
        profit_sharing_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        profit_sharing_entry = ttk.Entry(self, width=10, validate="key", validatecommand=(self.validate_input_func, "%P"))
        profit_sharing_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.cost_entries["profit_sharing"] = profit_sharing_entry

        profit_sharing_label = ttk.Label(
            self,
            text="Profit Sharing (USD/MT):",
            style="AdditionalCosts.TLabel"  # Use our new consistent style
        )
        profit_sharing_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        profit_sharing_brl_entry = ttk.Entry(self, width=10, validate="key", validatecommand=(self.validate_input_func, "%P"))
        profit_sharing_brl_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.cost_entries["profit_sharing_brl_per_sack"] = profit_sharing_brl_entry

        # Commodity Trader Commission
        commodity_trader_label = ttk.Label(
            self,
            text="Commodity Trader Commission (USD/MT):",
            style="AdditionalCosts.TLabel"
        ) # Use our new consistent style


        commodity_trader_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        commodity_trader_entry = ttk.Entry(self, width=10, validate="key", validatecommand=(self.validate_input_func, "%P"))
        commodity_trader_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.cost_entries["commodity_trader_commission"] = commodity_trader_entry

        # Ship Broker Commission
        ship_broker_label = ttk.Label(
            self,
            text="Ship Broker Commission (USD):",
            style="AdditionalCosts.TLabel"  # Use our new consistent style
        )

        ship_broker_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ship_broker_entry = ttk.Entry(self, width=10, validate="key", validatecommand=(self.validate_input_func, "%P"))
        ship_broker_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.cost_entries["ship_broker_commission"] = ship_broker_entry

    def get_additional_costs(self):
        """Retrieve values from additional cost entries."""
        additional_costs = {}
        for field_name, entry_widget in self.cost_entries.items():
            value = entry_widget.get()
            if value == "N/A":
                additional_costs[field_name] = 0.0  # Treat "N/A" as 0
            else:
                try:
                    additional_costs[field_name] = float(value) if value else 0.0  # Treat empty fields as 0
                except ValueError:
                    # Handle invalid input (e.g., non-numeric characters)
                    additional_costs[field_name] = 0.0
                    print(f"Invalid input for {field_name}: {value}")
        return additional_costs
