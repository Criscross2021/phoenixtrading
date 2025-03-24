import tkinter as tk
from tkinter import ttk
from trytond.pool import Pool
from trytond.transaction import Transaction

class TradeTerm:
    def __init__(self, root, update_input_boxes_callback):
        """
        Initialize the TradeTerm class.

        Args:
            root (tk.Tk): The root window or frame where the trade term buttons will be placed.
            update_input_boxes_callback (function): A callback function to update input boxes based on the selected trade term.
        """
        self.root = root
        self.update_input_boxes_callback = update_input_boxes_callback

        # Trade Term Frame
        self.trade_term_frame = ttk.Frame(root, style="White.TFrame")
        self.trade_term_frame.grid(row=1, column=0, sticky="w", padx=2, pady=2)

        # Trade Term Variable
        self.trade_term_var = tk.StringVar(value="FOB Storage")

        # Trade Term Buttons
        self.trade_term_buttons = []

        # Fetch trade terms from Tryton's database
        self.trade_terms = self.get_trade_terms()

        # Create buttons for each trade term
        for i, term in enumerate(self.trade_terms):
            button = ttk.Button(
                self.trade_term_frame, text=term, width=10, style="TButton",
                command=lambda t=term: self.select_trade_term(t)
            )
            button.grid(row=0, column=i, padx=2, pady=2)
            self.trade_term_buttons.append(button)

        # Set the initial trade term
        self.select_trade_term("FOB Storage")

    def get_trade_terms(self):
        """
        Fetch trade terms from the Tryton database.
        """
        try:
            with Transaction().start('database_name', 0, readonly=True) as transaction:
                TradeTerm = Pool().get('comerciointl_module.trade_term')
                trade_terms = TradeTerm.search([])
                return [term.name for term in trade_terms]
        except Exception as e:
            print(f"Error fetching trade terms: {e}")
            return ["FOB Storage", "FOB Port", "CIF Disport", "DDP"]  # Fallback to default terms

    def select_trade_term(self, term):
        """
        Select the trade term and update the input boxes.

        Args:
            term (str): The selected trade term (e.g., "FOB Storage").
        """
        print(f"Selected trade term: {term}")  # Debugging
        self.trade_term_var.set(term)

        # Call the callback function to update input boxes
        self.update_input_boxes_callback(term)

        # Reset all buttons to the default style
        for button in self.trade_term_buttons:
            button.config(style="TButton")
            print(f"Reset button: {button['text']} to TButton. Current style: {button['style']}")  # Debugging

        # Highlight the selected button
        selected_index = self.trade_terms.index(term)
        self.trade_term_buttons[selected_index].config(style="Selected.TButton")
        print(f"Highlighted button: {self.trade_term_buttons[selected_index]['text']} with Selected.TButton. Current style: {self.trade_term_buttons[selected_index]['style']}")  # Debugging