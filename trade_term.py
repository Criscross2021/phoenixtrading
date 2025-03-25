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
                self.trade_term_frame,
                text=term, width=10, style="TButton",
                command=lambda t=term: self.select_trade_term(t)
            )
            button.grid(row=0, column=i, padx=5, pady=5)
            self.trade_term_buttons.append(button)

        # Set the initial trade term
        self.select_trade_term("FOB Storage")

    def get_trade_terms(self):
        """Fetch trade terms with proper error handling"""
        try:
            # Initialize Tryton pool
            Pool.start()

            # Start transaction with proper connection check
            with Transaction().start('database_name', 0, readonly=True) as transaction:
                if not hasattr(transaction, '_datamanagers'):
                    print("No database connection available")
                    return self._get_default_terms()

                TradeTerm = Pool().get('comerciointl_module.trade_term')
                terms = TradeTerm.search([])
                return [term.name for term in terms] if terms else self._get_default_terms()

        except Exception as e:
            print(f"Error fetching trade terms: {e}")
            return self._get_default_terms()

    def _get_default_terms(self):
        """Fallback terms when database is unavailable"""
        return ["FOB Storage", "FOB Port", "CIF Disport", "DDP"]

    def _get_default_terms(self):
        """Fallback terms when database is unavailable"""
        return ["FOB Storage", "FOB Port", "CIF Disport", "DDP"]

    def select_trade_term(self, term):
        """Properly maintain button selection state with visual feedback"""
        self.trade_term_var.set(term)

        # Reset all buttons first
        for button in self.trade_term_buttons:
            button.state(['!pressed'])  # Clear pressed state
            button.configure(style="TButton")

        # Highlight selected button
        try:
            selected_index = self.trade_terms.index(term)
            self.trade_term_buttons[selected_index].state(['pressed'])
            self.trade_term_buttons[selected_index].configure(style="Selected.TButton")
        except ValueError:
            print(f"Trade term {term} not found in available terms")

        self.update_input_boxes_callback(term)