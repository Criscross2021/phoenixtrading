import tkinter as tk
from tkinter import ttk

class DisplayFrame:
    def __init__(self, root, calculate_costs_callback, reset_fields_callback):
        """
        Initialize the DisplayFrame class.

        Args:
            root (tk.Tk): The root window or frame where the display frame will be placed.
            calculate_costs_callback (function): Callback function for the Calculate Costs button.
            reset_fields_callback (function): Callback function for the Reset button.
        """
        self.root = root
        self.calculate_costs_callback = calculate_costs_callback
        self.reset_fields_callback = reset_fields_callback

        # Create the display frame
        self.frame = ttk.Frame(root, style="White.TFrame")  # Renamed to self.frame
        self.frame.grid(row=0, column=2, rowspan=50, sticky="nse", padx=10, pady=10)

        # Result Table
        self.result_table = ttk.Treeview(
            self.frame,  # Use self.frame instead of self.display_frame
            columns=("Cost Component", "Amount (USD)"),
            show="headings"
        )
        self.result_table.heading("Cost Component", text="Cost Component")
        self.result_table.heading("Amount (USD)", text="Amount (USD)")
        self.result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Total Costs Frame
        self.total_costs_frame = ttk.Frame(self.frame, style="White.TFrame")  # Use self.frame
        self.total_costs_frame.pack(side=tk.TOP, padx=2)

        # Total Cost Labels
        self.total_cost_usd_label = ttk.Label(self.total_costs_frame, text="Total Cost (USD):", style="Bold.TLabel")
        self.total_cost_usd_label.pack()
        self.total_cost_usd_value = ttk.Label(self.total_costs_frame, text="0.00", style="Bold.TLabel")
        self.total_cost_usd_value.pack()

        self.total_cost_brl_label = ttk.Label(self.total_costs_frame, text="Total Cost (BRL):", style="Bold.TLabel")
        self.total_cost_brl_label.pack()
        self.total_cost_brl_value = ttk.Label(self.total_costs_frame, text="0.00", style="Bold.TLabel")
        self.total_cost_brl_value.pack()

        self.total_cost_eur_label = ttk.Label(self.total_costs_frame, text="Total Cost (EUR):", style="Bold.TLabel")
        self.total_cost_eur_label.pack()
        self.total_cost_eur_value = ttk.Label(self.total_costs_frame, text="0.00", style="Bold.TLabel")
        self.total_cost_eur_value.pack()

        self.total_cost_yuan_label = ttk.Label(self.total_costs_frame, text="Total Cost (CNY):", style="Bold.TLabel")
        self.total_cost_yuan_label.pack()
        self.total_cost_yuan_value = ttk.Label(self.total_costs_frame, text="0.00", style="Bold.TLabel")
        self.total_cost_yuan_value.pack()

        # Buttons Frame
        self.buttons_frame = ttk.Frame(self.frame, style="White.TFrame")  # Use self.frame
        self.buttons_frame.pack(side=tk.TOP, pady=5)

        # Calculate Button
        self.calculate_button = ttk.Button(self.buttons_frame, text="Calculate Costs", command=self.calculate_costs_callback)
        self.calculate_button.pack(side=tk.LEFT, padx=3)

        # Reset Button
        self.reset_button = ttk.Button(self.buttons_frame, text="Reset", command=self.reset_fields_callback)
        self.reset_button.pack(side=tk.BOTTOM, padx=5)

    def update_result_table(self, cost_breakdown):
        """
        Update the result table with the cost breakdown.

        Args:
            cost_breakdown (dict): A dictionary containing the cost breakdown.
        """
        # Clear existing rows
        for row in self.result_table.get_children():
            self.result_table.delete(row)

        # Insert new rows
        for field_name, value in cost_breakdown.items():
            self.result_table.insert("", "end", values=(field_name, f"{value:.2f}"))

    def update_total_costs(self, total_cost_usd, total_cost_brl, total_cost_eur, total_cost_yuan):
        """
        Update the total cost labels.

        Args:
            total_cost_usd (float): Total cost in USD.
            total_cost_brl (float): Total cost in BRL.
            total_cost_eur (float): Total cost in EUR.
            total_cost_yuan (float): Total cost in CNY.
        """
        self.total_cost_usd_value.config(text=f"{total_cost_usd:.2f}")
        self.total_cost_brl_value.config(text=f"{total_cost_brl:.2f}")
        self.total_cost_eur_value.config(text=f"{total_cost_eur:.2f}")
        self.total_cost_yuan_value.config(text=f"{total_cost_yuan:.2f}")