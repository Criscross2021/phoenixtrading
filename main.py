import tkinter as tk
from tkinter import ttk, messagebox
from sale_details.sale_manager import SaleManager
from display_frame.display_frame import DisplayFrame
from trade_term.trade_term import TradeTerm
from commodity.commodity import CommoditySelection
from cost_input.cost_input import CostInput
from commodity.trade_logic.commodity_trade import CommodityTrade
from logo_frame.logo import Logo
from cost_input.additional_costs_frame import AdditionalCostsFrame

class MainApp:
    def __init__(self, root):
        """
        Initialize the MainApp class.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("Commodity Trade Logistics Calculator")
        self.root.geometry("1600x900")
        self.root.configure(bg="white")
        self.root.resizable(True, True)

        # Initialize the style variable
        self.style = ttk.Style()

        # Configure the root window's grid to expand
        self.root.grid_rowconfigure(1, weight=1)  # Make row 1 expandable
        self.root.grid_columnconfigure(0, weight=1)  # Make column 0 expandable

        # Configure styles
        self.configure_styles()

        # Load and display the logo in the root window (above the notebook)
        self.load_logo()

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Initialize the CommodityTrade class FIRST
        self.trade = CommodityTrade()

        # Main Frame (Tab 1)
        self.main_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.main_frame, text="Main")

        # Configure the main_frame's grid
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create content frame (no scrollbar)
        self.content_frame = ttk.Frame(self.main_frame, style="White.TFrame")
        self.content_frame.grid(row=0, column=0, sticky="nsew")

        # Initialize DisplayFrame
        self.display_frame = DisplayFrame(
            self.main_frame,
            calculate_costs_callback=self.calculate_costs,
            reset_fields_callback=self.reset_fields
        )

        # Initialize components in content_frame
        self.commodity_selection = CommoditySelection(
            self.content_frame,
            self.update_units,
            self.trade.UNIT_CONVERSIONS
        )

        self.cost_input = CostInput(
            self.content_frame,
            self.validate_input_func,
            self.trade
        )

        self.trade_term = TradeTerm(
            self.content_frame,
            self.update_input_boxes
        )

        # Initialize SaleManager in Sale Details tab
        self.sale_details_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.sale_details_frame, text="Sale Details")
        self.sale_manager = SaleManager(self.sale_details_frame)
        self.sale_manager.create_sale_details_frame()

        # Additional Costs Frame
        self.additional_costs_frame = AdditionalCostsFrame(
            self.main_frame,
            self.validate_input_func
        )
        self.additional_costs_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def configure_styles(self):
        """Configure the styles for the application."""
        # Frame and label styles
        self.style.configure("White.TFrame", background="white")
        self.style.configure("White.TLabel",
                             background="white",
                             font=("Arial", 11),
                             foreground="black")
        self.style.configure("GroupTitle.TLabel",
                             background="white",
                             font=("Arial", 10, "bold"),
                             foreground="black")
        self.style.configure("White.TEntry",
                             background="white",
                             font=("Arial", 11),
                             foreground="black")
        self.style.configure("Bold.TLabel",
                             background="white",
                             font=("Arial", 11, "bold"),
                             foreground="red")

        # Additional Costs Frame style
        self.style.configure("AdditionalCosts.TLabel",
                             background="white",
                             font=("Arial", 11),
                             foreground="black")

        # Button styles
        self.style.configure("TButton",
                             background="#e0e0e0",
                             foreground="black",
                             font=("Arial", 11),
                             padding=6,
                             relief="groove",
                             focuscolor="#4a7dc9")  # Focus color added here

        self.style.configure("Selected.TButton",
                             background="#4a7dc9",
                             foreground="white",
                             relief="sunken",
                             focuscolor="#3a6cb5")  # Darker focus color for selected

        # Hover and focus effects
        self.style.map("TButton",
                       background=[("active", "#d0d0d0"), ("focus", "#e0e0e0")],
                       relief=[("pressed", "sunken"), ("!pressed", "groove")],
                       focuscolor=[("focus", "#4a7dc9"), ("!focus", "")])  # Focus ring control

        # Combobox styles
        self.style.configure("TCombobox.Button",
                             background="#4a7dc9",
                             padding=5,
                             focuscolor="#3a6cb5")

    def load_logo(self):
        self.style.configure("Transparent.TLabel",
                             background="white",
                             borderwidth=0,
                             padding=0)

        """Load and display the logo in the root window."""
        logo_path = "/Users/user/PycharmProjects/ComercioIntl/logo_frame/phoenixlogo.png"  # Update this path
        logo = Logo(self.root, logo_path)
        logo_label = logo.load_logo()
        logo_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    def calculate_costs(self):
        """Calculate the total costs and update the display frame."""
        try:
            # Retrieve quantity and other inputs
            quantity = self.commodity_selection.get_quantity()
            costs = self.get_cost_entries()

            # Retrieve additional costs from the AdditionalCostsFrame
            additional_costs = self.additional_costs_frame.get_additional_costs()

            # Merge additional costs with other cost parameters
            costs.update(additional_costs)

            # Calculate total cost using the CommodityTrade class
            selected_commodity = self.commodity_selection.commodity_var.get()
            selected_unit = self.commodity_selection.unit_var.get()
            selected_trade_term = self.trade_term.trade_term_var.get()
            cost_breakdown = self.trade.calculate_total_cost(
                quantity, selected_unit, selected_commodity, selected_trade_term, costs
            )

            # Update the display frame
            self.display_frame.update_result_table(cost_breakdown)
            self.display_frame.update_total_costs(
                cost_breakdown["Total Cost (USD)"],
                cost_breakdown["Total Cost (BRL)"],
                cost_breakdown["Total Cost (EUR)"],
                cost_breakdown["Total Cost (CNY)"]
            )

        except ValueError:
            # Handle invalid input
            messagebox.showerror("Error", "Please enter valid numbers in all fields.")

    def reset_fields(self):
        """Reset all input fields and clear the result table."""
        self.sale_manager.reset_fields()
        self.display_frame.update_result_table({})
        self.display_frame.update_total_costs(0.00, 0.00, 0.00, 0.00)

    def get_cost_entries(self):
        """Retrieve values from cost entries."""
        costs = {}
        for field_name, entry_widget in self.cost_input.cost_entries.items():
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

    def update_input_boxes(self, term):
        """Update the input boxes based on the selected trade term."""
        self.cost_input.update_input_boxes(term)  # Call the update_input_boxes method in CostInput

    def update_units(self, event=None):
        """Update the unit dropdown options based on the selected commodity."""
        self.commodity_selection.update_units(event)

    def validate_input(self, char):
        """Validate input to allow numbers, one decimal point, and empty input."""
        if char == "":  # Allow empty input (e.g., when deleting all characters)
            return True
        if char.replace(".", "", 1).isdigit() and len(char) <= 6:  # Allow numbers and one decimal point
            return True
        return False

    @property
    def validate_input_func(self):
        """Return the validation function."""
        return self.root.register(self.validate_input)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)

    root.mainloop()
