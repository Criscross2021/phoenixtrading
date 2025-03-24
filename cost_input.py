import tkinter as tk
from tkinter import ttk
from cost_input.cost_breakdown import CostBreakdown

class CostInput:
    def __init__(self, root, validate_input_func, trade):
        """
        Initialize the CostInput class.

        Args:
            root (tk.Tk): The root window or frame where the cost input fields will be placed.
            validate_input_func (function): Function to validate input in the cost fields.
            trade (CommodityTrade): An instance of the CommodityTrade class.
        """
        self.root = root
        self.validate_input_func = validate_input_func
        self.trade = trade
        self.cost_entries = {}
        self.cost_field_groups = []

        # Create a frame to hold all the cost input fields
        self.frame = ttk.Frame(root, style="White.TFrame")
        self.frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        # Define cost field groups
        self.cost_fields_group1 = [
            ("Purchase Price (per unit):", "purchase_price_per_unit"),
            ("Processing Fee (per unit):", "processing_fee_per_unit"),
            ("Trucking (Farm to Storage) (per unit):", "trucking_farm_to_storage_per_unit"),
            ("Storage Fee (Farm) (per unit):", "storage_fee_per_unit"),
            ("Loading the containers (in RLS):", "loading_containers_rls"),
        ]

        self.cost_fields_group2 = [
            # Truck-related fields
            ("Trucking (Storage to Port) (per unit):", "trucking_storage_to_port_per_unit"),
            ("Free Time at load by Trucks (hours):", "truck_free_time_hours"),
            ("Free Time at load by Trucks (extra in RLS):", "truck_free_time_rls"),
            ("Collecting empty Containers:", "empty_containers"),
            ("Unloading the containers (extra in RLS):", "truck_unloading_rls"),

            # Terminal-related fields
            ("Free Time at load by TERMINAL (days):", "terminal_free_time_days"),
            ("Storage Fee (Port) (per unit):", "storage_fee_port_per_unit"),
            ("Port Handling (per unit):", "port_handling_per_unit"),

            # Taxes and fees
            ("Ad Valorem:", "ad_valorem"),
            ("ICMS:", "ICMS_unit"),
        ]

        self.cost_fields_group3 = [
            # Ocean freight and related fees
            ("Ocean Freight (per tonne):", "ocean_freight_per_tonne"),
            ("Carrier Security Fee (CSF) (per tonne):", "carrier_security_fee_per_tonne"),
            ("Bunker Recovery Charge (BRC) (per tonne):", "bunker_recovery_charge_per_tonne"),
            ("Pilotage Service Cost (PSC) (per tonne):", "pilotage_service_cost_per_tonne"),

            # Demurrage and detention at load
            ("Demurrage Rate at load (per day):", "demurrage_load_per_day"),
            ("Demurrage Days at load:", "demurrage_load_days"),
            ("Detention Rate at load (per day):", "detention_load_per_day"),
            ("Detention Days at load:", "detention_load_days"),

            # Ship owner-related fields
            ("Free Time at load by Ship Owner (days):", "ship_owner_free_time_days"),

            # Terminal handling and security
            ("Terminal Handling Charge (THC) - Load (per tonne):", "terminal_handling_charge_load_per_tonne"),
            ("Ship and Port Security (SPS) (per tonne):", "ship_port_security_per_tonne"),

            # Documentation and insurance
            ("Documentation Fee (DOC):", "documentation_fee"),
            ("Seal Fee (SEL):", "seal_fee"),
            ("Insurance Fee (per tonne):", "insurance_per_tonne"),
        ]

        self.cost_fields_group4 = [
            # Destination-related fields
            ("Terminal Handling Charge (THC) - Disport (per tonne):", "terminal_handling_charge_disport_per_tonne"),
            ("Delivery Order Fee (DOF):", "delivery_order_fee"),
            ("Inland Transport (Destination) (per tonne):", "inland_transport_destination_per_tonne"),
            ("Storage Fee at Destination (per tonne):", "storage_fee_destination_per_tonne"),
            ("Detention Days at Destination:", "detention_discharge_days"),
        ]

        # Combine all cost field groups
        self.cost_field_groups = [
            self.cost_fields_group1,
            self.cost_fields_group2,
            self.cost_fields_group3,
            self.cost_fields_group4,
        ]

        # Create input fields for cost parameters
        self.create_cost_input_fields()

    def create_cost_input_fields(self):
        """Create input fields for cost parameters."""
        # Group 1: Trade (Columns 0 and 1)
        group1_label = ttk.Label(self.frame, text="Trade", style="GroupTitle.TLabel")
        group1_label.grid(row=0, column=0, sticky=tk.W, pady=(5, 0))
        row_start_group1 = 1  # Start Group 1 at row 1
        for i, (label_text, field_name) in enumerate(self.cost_fields_group1):
            label = ttk.Label(self.frame, text=label_text, style="White.TLabel")
            label.grid(row=row_start_group1 + i, column=0, sticky=tk.W)
            entry = ttk.Entry(self.frame, width=8, validate="key", validatecommand=(self.validate_input_func, "%P"),
                              style="White.TEntry")
            entry.grid(row=row_start_group1 + i, column=1, sticky=tk.W)
            self.cost_entries[field_name] = entry

        # Group 2: Inland (Columns 0 and 1)
        group2_label = ttk.Label(self.frame, text="Inland", style="GroupTitle.TLabel")
        group2_label.grid(row=row_start_group1 + len(self.cost_fields_group1), column=0, sticky=tk.W, pady=(5, 0))
        row_start_group2 = row_start_group1 + len(self.cost_fields_group1) + 1  # Start Group 2 after Group 1
        for i, (label_text, field_name) in enumerate(self.cost_fields_group2):
            label = ttk.Label(self.frame, text=label_text, style="White.TLabel")
            label.grid(row=row_start_group2 + i, column=0, sticky=tk.W)
            entry = ttk.Entry(self.frame, width=8, validate="key", validatecommand=(self.validate_input_func, "%P"),
                              style="White.TEntry")
            entry.grid(row=row_start_group2 + i, column=1, sticky=tk.W)
            self.cost_entries[field_name] = entry

        # Group 3: CIF/DDP Ocean (Columns 2 and 3)
        group3_label = ttk.Label(self.frame, text="CIF/DDP Ocean", style="GroupTitle.TLabel")
        group3_label.grid(row=0, column=2, sticky=tk.W, pady=(5, 0))
        row_start_group3 = 1  # Start Group 3 at row 1
        for i, (label_text, field_name) in enumerate(self.cost_fields_group3):
            label = ttk.Label(self.frame, text=label_text, style="White.TLabel")
            label.grid(row=row_start_group3 + i, column=2, sticky=tk.W)
            entry = ttk.Entry(self.frame, width=8, validate="key", validatecommand=(self.validate_input_func, "%P"),
                              style="White.TEntry")
            entry.grid(row=row_start_group3 + i, column=3, sticky=tk.W)
            self.cost_entries[field_name] = entry

        # Group 4: Destination (Columns 2 and 3)
        group4_label = ttk.Label(self.frame, text="Destination", style="GroupTitle.TLabel")
        group4_label.grid(row=row_start_group3 + len(self.cost_fields_group3), column=2, sticky=tk.W, pady=(5, 0))
        row_start_group4 = row_start_group3 + len(self.cost_fields_group3) + 1  # Start Group 4 after Group 3
        for i, (label_text, field_name) in enumerate(self.cost_fields_group4):
            label = ttk.Label(self.frame, text=label_text, style="White.TLabel")
            label.grid(row=row_start_group4 + i, column=2, sticky=tk.W)
            entry = ttk.Entry(self.frame, width=8, validate="key", validatecommand=(self.validate_input_func, "%P"),
                              style="White.TEntry")
            entry.grid(row=row_start_group4 + i, column=3, sticky=tk.W)
            self.cost_entries[field_name] = entry

    def get_cost_entries(self):
        """Retrieve values from cost entries."""
        costs = {}
        for field_name, entry_widget in self.cost_entries.items():
            value = entry_widget.get()
            if value == "N/A":
                costs[field_name] = 0.0  # Treat "N/A" as 0
            else:
                try:
                    costs[field_name] = float(value) if value else 0.0  # Treat empty fields as 0
                except ValueError:
                    # Handle invalid input (e.g., non-numeric characters)
                    costs[field_name] = 0.0
                    print(f"Invalid input for {field_name}: {value}")
        return costs

    def update_input_boxes(self, trade_term):
        """
        Enable/disable fields based on the selected trade term.

        Args:
            trade_term (str): The selected trade term (e.g., "FOB Storage").
        """
        if trade_term == "FOB Storage":
            # Enable fields in cost_fields_group1
            for label_text, field_name in self.cost_fields_group1:
                self.cost_entries[field_name].config(state="normal")
                if self.cost_entries[field_name].get() == "N/A":  # Clear "N/A" if applicable
                    self.cost_entries[field_name].delete(0, tk.END)
            # Disable fields in other groups
            for group in self.cost_field_groups[1:]:
                for label_text, field_name in group:
                    self.cost_entries[field_name].config(state="disabled")
                    self.cost_entries[field_name].delete(0, tk.END)
                    self.cost_entries[field_name].insert(0, "N/A")
        elif trade_term == "FOB Port":
            # Enable fields in cost_fields_group1 and cost_fields_group2
            for group in self.cost_field_groups[:2]:
                for label_text, field_name in group:
                    self.cost_entries[field_name].config(state="normal")
                    if self.cost_entries[field_name].get() == "N/A":  # Clear "N/A" if applicable
                        self.cost_entries[field_name].delete(0, tk.END)
            # Disable fields in cost_fields_group3 and cost_fields_group4
            for group in self.cost_field_groups[2:]:
                for label_text, field_name in group:
                    self.cost_entries[field_name].config(state="disabled")
                    self.cost_entries[field_name].delete(0, tk.END)
                    self.cost_entries[field_name].insert(0, "N/A")
        elif trade_term == "CIF Disport":
            # Enable fields in cost_fields_group1, cost_fields_group2, and cost_fields_group3
            for group in self.cost_field_groups[:3]:
                for label_text, field_name in group:
                    self.cost_entries[field_name].config(state="normal")
                    if self.cost_entries[field_name].get() == "N/A":  # Clear "N/A" if applicable
                        self.cost_entries[field_name].delete(0, tk.END)
            # Disable fields in cost_fields_group4
            for label_text, field_name in self.cost_field_groups[3]:
                self.cost_entries[field_name].config(state="disabled")
                self.cost_entries[field_name].delete(0, tk.END)
                self.cost_entries[field_name].insert(0, "N/A")
        elif trade_term == "DDP":
            # Enable all fields
            for group in self.cost_field_groups:
                for label_text, field_name in group:
                    self.cost_entries[field_name].config(state="normal")
                    if self.cost_entries[field_name].get() == "N/A":  # Clear "N/A" if applicable
                        self.cost_entries[field_name].delete(0, tk.END)