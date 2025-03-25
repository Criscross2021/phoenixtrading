import tkinter as tk
from tkinter import ttk
from cost_input.cost_breakdown import CostBreakdown


class CostInput:
    def __init__(self, root, validate_input_func, trade):
        """
        Initialize the CostInput class with currency selection.

        Args:
            root (tk.Tk): The root window or frame.
            validate_input_func (function): Input validation function.
            trade (CommodityTrade): Trade instance for unit conversions.
        """
        self.root = root
        self.validate_input_func = validate_input_func
        self.trade = trade
        self.cost_entries = {}
        self.currency_vars = {}
        self.cost_field_groups = []

        # Create main frame
        self.frame = ttk.Frame(root, style="White.TFrame")
        self.frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        # Define cost field groups with default currencies
        self.cost_fields_group1 = [
            ("Purchase Price:", "purchase_price", "BRL"),
            ("Processing Fee:", "processing_fee", "BRL"),
            ("Trucking (Farm to Storage):", "trucking_farm_to_storage", "BRL"),
            ("Storage Fee (Farm):", "storage_fee_farm", "BRL"),
            ("Loading Containers:", "loading_containers", "BRL")
        ]

        self.cost_fields_group2 = [
            # Truck-related fields
            ("Trucking (Storage to Port):", "trucking_storage_to_port", "BRL"),
            ("Free Time at Load (Hours):", "truck_free_time_hours", "BRL"),
            ("Free Time at Load (RLS):", "truck_free_time_rls", "BRL"),
            ("Empty Containers:", "empty_containers", "BRL"),
            ("Unloading Containers:", "unloading_containers", "BRL"),

            # Terminal-related fields
            ("Free Time at Terminal (Days):", "terminal_free_time_days", "USD"),
            ("Storage Fee (Port):", "storage_fee_port", "USD"),
            ("Port Handling:", "port_handling", "USD"),

            # Taxes and fees
            ("Ad Valorem:", "ad_valorem", "USD"),
            ("ICMS:", "icms", "USD"),
        ]

        self.cost_fields_group3 = [
            # Ocean freight and related fees
            ("Ocean Freight:", "ocean_freight", "USD"),
            ("Carrier Security Fee:", "carrier_security_fee", "USD"),
            ("Bunker Recovery Charge:", "bunker_recovery_charge", "USD"),
            ("Pilotage Service Cost:", "pilotage_service_cost", "USD"),

            # Demurrage and detention
            ("Demurrage Rate:", "demurrage_rate", "USD"),
            ("Demurrage Days:", "demurrage_days", "USD"),
            ("Detention Rate:", "detention_rate", "USD"),
            ("Detention Days:", "detention_days", "USD"),

            # Ship owner-related fields
            ("Ship Owner Free Time:", "ship_owner_free_time", "USD"),

            # Terminal handling and security
            ("Terminal Handling Charge:", "terminal_handling_charge", "USD"),
            ("Ship and Port Security:", "ship_port_security", "USD"),

            # Documentation and insurance
            ("Documentation Fee:", "documentation_fee", "USD"),
            ("Seal Fee:", "seal_fee", "USD"),
            ("Insurance:", "insurance", "USD"),
        ]

        self.cost_fields_group4 = [
            # Destination-related fields
            ("Terminal Handling (Disport):", "terminal_handling_disport", "USD"),
            ("Delivery Order Fee:", "delivery_order_fee", "USD"),
            ("Inland Transport (Destination):", "inland_transport_destination", "USD"),
            ("Storage Fee (Destination):", "storage_fee_destination", "USD"),
            ("Detention at Destination:", "detention_destination", "USD"),
        ]

        # Combine all groups
        self.cost_field_groups = [
            self.cost_fields_group1,
            self.cost_fields_group2,
            self.cost_fields_group3,
            self.cost_fields_group4,
        ]

        # Create input fields with currency dropdowns
        self.create_cost_input_fields()

    def create_cost_input_fields(self):
        """Create input fields with currency dropdowns."""
        # Group 1: Farm Costs (Columns 0-2)
        group1_label = ttk.Label(self.frame, text="Farm Costs", style="GroupTitle.TLabel")
        group1_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        for i, (label_text, field_name, default_currency) in enumerate(self.cost_fields_group1, start=1):
            self._create_field_row(row=i, col=0, label_text=label_text,
                                   field_name=field_name, default_currency=default_currency)

        # Group 2: Inland Transport (Columns 0-2)
        group2_label = ttk.Label(self.frame, text="Inland Transport", style="GroupTitle.TLabel")
        group2_label.grid(row=len(self.cost_fields_group1) + 1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))

        for i, (label_text, field_name, default_currency) in enumerate(self.cost_fields_group2,
                                                                       start=len(self.cost_fields_group1) + 2):
            self._create_field_row(row=i, col=0, label_text=label_text,
                                   field_name=field_name, default_currency=default_currency)

        # Group 3: Ocean Freight (Columns 3-5)
        group3_label = ttk.Label(self.frame, text="Ocean Freight", style="GroupTitle.TLabel")
        group3_label.grid(row=0, column=3, columnspan=3, sticky=tk.W, pady=(5, 0))

        for i, (label_text, field_name, default_currency) in enumerate(self.cost_fields_group3, start=1):
            self._create_field_row(row=i, col=3, label_text=label_text,
                                   field_name=field_name, default_currency=default_currency)

        # Group 4: Destination Costs (Columns 3-5)
        group4_label = ttk.Label(self.frame, text="Destination Costs", style="GroupTitle.TLabel")
        group4_label.grid(row=len(self.cost_fields_group3) + 1, column=3, columnspan=3, sticky=tk.W, pady=(10, 0))

        for i, (label_text, field_name, default_currency) in enumerate(self.cost_fields_group4,
                                                                       start=len(self.cost_fields_group3) + 2):
            self._create_field_row(row=i, col=3, label_text=label_text,
                                   field_name=field_name, default_currency=default_currency)

    def _create_field_row(self, row, col, label_text, field_name, default_currency):
        """Create a label + entry + currency dropdown row."""
        # Label
        label = ttk.Label(self.frame, text=label_text, style="White.TLabel")
        label.grid(row=row, column=col, sticky=tk.W, padx=5)

        # Entry field
        entry = ttk.Entry(self.frame, width=10, validate="key",
                          validatecommand=(self.validate_input_func, "%P"))
        entry.grid(row=row, column=col + 1, sticky=tk.W)
        self.cost_entries[field_name] = entry

        # Currency dropdown
        currency_var = tk.StringVar(value=default_currency)
        currency_dropdown = ttk.Combobox(
            self.frame,
            textvariable=currency_var,
            values=["BRL", "USD"],
            width=4,
            state="readonly"
        )
        currency_dropdown.grid(row=row, column=col + 2, sticky=tk.W, padx=5)
        self.currency_vars[field_name] = currency_var

    def get_cost_entries(self):
        """Returns {field_name: (value, currency)} with validation."""
        costs = {}
        for field_name, entry in self.cost_entries.items():
            value = entry.get()
            currency = self.currency_vars[field_name].get()

            if value == "N/A":
                costs[field_name] = (0.0, currency)
            else:
                try:
                    costs[field_name] = (float(value) if value else 0.0, currency)
                except ValueError:
                    print(f"Invalid input for {field_name}: {value}")
                    costs[field_name] = (0.0, currency)
        return costs

    def update_input_boxes(self, trade_term):
        """Enable/disable fields based on trade term (preserves currency selections)."""
        # Define which groups to enable for each trade term
        term_rules = {
            "FOB Storage": [0],  # Only group1 (Farm)
            "FOB Port": [0, 1],  # Farm + Inland
            "CIF Disport": [0, 1, 2],  # Farm + Inland + Ocean
            "DDP": [0, 1, 2, 3]  # All groups
        }

        # First disable all fields
        for field_name in self.cost_entries:
            self.cost_entries[field_name].config(state="disabled")
            self.cost_entries[field_name].delete(0, tk.END)
            self.cost_entries[field_name].insert(0, "N/A")

        # Enable fields for selected trade term
        for group_idx in term_rules[trade_term]:
            for (label_text, field_name, currency) in self.cost_field_groups[group_idx]:
                self.cost_entries[field_name].config(state="normal")
                self.cost_entries[field_name].delete(0, tk.END)