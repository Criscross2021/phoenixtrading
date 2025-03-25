import tkinter as tk
from tkinter import ttk, messagebox
from trytond.pool import Pool
from trytond.transaction import Transaction
from datetime import datetime
import uuid
import os

class SaleManager:
    def __init__(self, root):
        """
        Initialize the SaleManager class.

        Args:
            root (tk.Tk): The root window or frame where the sale details will be displayed.
        """
        self.root = root
        self.current_sale_id = None  # Track the current sale being edited
        self.create_sale_details_frame()

    def create_sale_details_frame(self):
        """
        Create and return the sale details frame.

        Returns:
            ttk.Frame: The frame containing all sale details widgets.
        """
        sale_details_frame = ttk.LabelFrame(self.root, text="Sale Details", padding="10")
        sale_details_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Date
        label_date = ttk.Label(sale_details_frame, text="Date:")
        label_date.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_date = ttk.Entry(sale_details_frame, width=30)
        self.entry_date.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today's date

        # Invoice Number
        label_invoice_number = ttk.Label(sale_details_frame, text="Invoice Number:")
        label_invoice_number.grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_invoice_number = ttk.Entry(sale_details_frame, width=30)
        self.entry_invoice_number.grid(row=0, column=3, sticky=tk.W, pady=5)

        # Product
        label_product = ttk.Label(sale_details_frame, text="Product:")
        label_product.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_product = ttk.Entry(sale_details_frame, width=30)
        self.entry_product.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Quantity
        label_quantity = ttk.Label(sale_details_frame, text="Quantity:")
        label_quantity.grid(row=1, column=2, sticky=tk.W, pady=5)
        self.entry_quantity = ttk.Entry(sale_details_frame, width=30)
        self.entry_quantity.grid(row=1, column=3, sticky=tk.W, pady=5)

        # Load Port
        label_load_port = ttk.Label(sale_details_frame, text="Load Port:")
        label_load_port.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_load_port = ttk.Entry(sale_details_frame, width=30)
        self.entry_load_port.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Destination
        label_destination = ttk.Label(sale_details_frame, text="Destination:")
        label_destination.grid(row=2, column=2, sticky=tk.W, pady=5)
        self.entry_destination = ttk.Entry(sale_details_frame, width=30)
        self.entry_destination.grid(row=2, column=3, sticky=tk.W, pady=5)

        # Selling Price
        label_selling_price = ttk.Label(sale_details_frame, text="Selling Price:")
        label_selling_price.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_selling_price = ttk.Entry(sale_details_frame, width=30)
        self.entry_selling_price.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Total Cost
        label_total_cost = ttk.Label(sale_details_frame, text="Total Cost:")
        label_total_cost.grid(row=3, column=2, sticky=tk.W, pady=5)
        self.entry_total_cost = ttk.Entry(sale_details_frame, width=30)
        self.entry_total_cost.grid(row=3, column=3, sticky=tk.W, pady=5)

        # Farmer Details
        label_farmer_name = ttk.Label(sale_details_frame, text="Farmer Name:")
        label_farmer_name.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_farmer_name = ttk.Entry(sale_details_frame, width=30)
        self.entry_farmer_name.grid(row=4, column=1, sticky=tk.W, pady=5)

        label_farmer_email = ttk.Label(sale_details_frame, text="Farmer Email:")
        label_farmer_email.grid(row=4, column=2, sticky=tk.W, pady=5)
        self.entry_farmer_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_farmer_email.grid(row=4, column=3, sticky=tk.W, pady=5)

        # Storage Details
        label_storage_name = ttk.Label(sale_details_frame, text="Storage Name:")
        label_storage_name.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_storage_name = ttk.Entry(sale_details_frame, width=30)
        self.entry_storage_name.grid(row=5, column=1, sticky=tk.W, pady=5)

        label_storage_email = ttk.Label(sale_details_frame, text="Storage Email:")
        label_storage_email.grid(row=5, column=2, sticky=tk.W, pady=5)
        self.entry_storage_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_storage_email.grid(row=5, column=3, sticky=tk.W, pady=5)

        # Buyer Details
        label_buyer_name = ttk.Label(sale_details_frame, text="Buyer Name:")
        label_buyer_name.grid(row=6, column=0, sticky=tk.W, pady=5)
        self.entry_buyer_name = ttk.Entry(sale_details_frame, width=30)
        self.entry_buyer_name.grid(row=6, column=1, sticky=tk.W, pady=5)

        label_buyer_email = ttk.Label(sale_details_frame, text="Buyer Email:")
        label_buyer_email.grid(row=6, column=2, sticky=tk.W, pady=5)
        self.entry_buyer_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_buyer_email.grid(row=6, column=3, sticky=tk.W, pady=5)

        # Logistics Company
        label_logistics_company = ttk.Label(sale_details_frame, text="Logistics Company:")
        label_logistics_company.grid(row=7, column=0, sticky=tk.W, pady=5)
        self.entry_logistics_company = ttk.Entry(sale_details_frame, width=30)
        self.entry_logistics_company.grid(row=7, column=1, sticky=tk.W, pady=5)

        label_logistics_email = ttk.Label(sale_details_frame, text="Logistics Email:")
        label_logistics_email.grid(row=7, column=2, sticky=tk.W, pady=5)
        self.entry_logistics_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_logistics_email.grid(row=7, column=3, sticky=tk.W, pady=5)

        # Multilog Company
        label_multilog_company = ttk.Label(sale_details_frame, text="Multilog Company:")
        label_multilog_company.grid(row=8, column=0, sticky=tk.W, pady=5)
        self.entry_multilog_company = ttk.Entry(sale_details_frame, width=30)
        self.entry_multilog_company.grid(row=8, column=1, sticky=tk.W, pady=5)

        label_multilog_email = ttk.Label(sale_details_frame, text="Multilog Email:")
        label_multilog_email.grid(row=8, column=2, sticky=tk.W, pady=5)
        self.entry_multilog_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_multilog_email.grid(row=8, column=3, sticky=tk.W, pady=5)

        # Freight Forwarder
        label_freight_forwarder = ttk.Label(sale_details_frame, text="Freight Forwarder:")
        label_freight_forwarder.grid(row=9, column=0, sticky=tk.W, pady=5)
        self.entry_freight_forwarder = ttk.Entry(sale_details_frame, width=30)
        self.entry_freight_forwarder.grid(row=9, column=1, sticky=tk.W, pady=5)

        label_freight_forwarder_email = ttk.Label(sale_details_frame, text="Freight Forwarder Email:")
        label_freight_forwarder_email.grid(row=9, column=2, sticky=tk.W, pady=5)
        self.entry_freight_forwarder_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_freight_forwarder_email.grid(row=9, column=3, sticky=tk.W, pady=5)

        # Commodity Broker
        label_commodity_broker = ttk.Label(sale_details_frame, text="Commodity Broker:")
        label_commodity_broker.grid(row=10, column=0, sticky=tk.W, pady=5)
        self.entry_commodity_broker = ttk.Entry(sale_details_frame, width=30)
        self.entry_commodity_broker.grid(row=10, column=1, sticky=tk.W, pady=5)

        label_commodity_broker_email = ttk.Label(sale_details_frame, text="Commodity Broker Email:")
        label_commodity_broker_email.grid(row=10, column=2, sticky=tk.W, pady=5)
        self.entry_commodity_broker_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_commodity_broker_email.grid(row=10, column=3, sticky=tk.W, pady=5)

        # Ship Broker
        label_ship_broker = ttk.Label(sale_details_frame, text="Ship Broker:")
        label_ship_broker.grid(row=11, column=0, sticky=tk.W, pady=5)
        self.entry_ship_broker = ttk.Entry(sale_details_frame, width=30)
        self.entry_ship_broker.grid(row=11, column=1, sticky=tk.W, pady=5)

        label_ship_broker_email = ttk.Label(sale_details_frame, text="Ship Broker Email:")
        label_ship_broker_email.grid(row=11, column=2, sticky=tk.W, pady=5)
        self.entry_ship_broker_email = ttk.Entry(sale_details_frame, width=30)
        self.entry_ship_broker_email.grid(row=11, column=3, sticky=tk.W, pady=5)

        # Upload Documents Button
        upload_button = ttk.Button(sale_details_frame, text="Upload Documents", command=self.upload_documents)
        upload_button.grid(row=12, column=0, columnspan=2, pady=10)

        # Execute Sale Button
        execute_sale_button = ttk.Button(sale_details_frame, text="Execute Sale", command=self.execute_sale)
        execute_sale_button.grid(row=12, column=2, columnspan=2, pady=10)

        # Search Frame
        search_frame = ttk.LabelFrame(sale_details_frame, text="Search Sales", padding="10")
        search_frame.grid(row=13, column=0, columnspan=4, sticky="ew", pady=10)

        # Search by Sale ID
        label_search_sale_id = ttk.Label(search_frame, text="Search by Sale ID:")
        label_search_sale_id.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_search_sale_id = ttk.Entry(search_frame, width=20)
        self.entry_search_sale_id.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Search by Date
        label_search_date = ttk.Label(search_frame, text="Search by Date:")
        label_search_date.grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_search_date = ttk.Entry(search_frame, width=20)
        self.entry_search_date.grid(row=0, column=3, sticky=tk.W, pady=5)

        # Search by Buyer's Name
        label_search_buyer_name = ttk.Label(search_frame, text="Search by Buyer's Name:")
        label_search_buyer_name.grid(row=0, column=4, sticky=tk.W, pady=5)
        self.entry_search_buyer_name = ttk.Entry(search_frame, width=20)
        self.entry_search_buyer_name.grid(row=0, column=5, sticky=tk.W, pady=5)

        # Search Button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_sales)
        search_button.grid(row=0, column=6, sticky=tk.W, padx=5, pady=5)

        return sale_details_frame

    def execute_sale(self):
        """
        Finalize the sale and store details in the Tryton database.
        """
        try:
            # Validate inputs
            entries = {
                "farmer_email": self.entry_farmer_email,
                "storage_email": self.entry_storage_email,
                "buyer_email": self.entry_buyer_email,
                "logistics_email": self.entry_logistics_email,
                "multilog_email": self.entry_multilog_email,
                "freight_forwarder_email": self.entry_freight_forwarder_email,
                "commodity_broker_email": self.entry_commodity_broker_email,
                "ship_broker_email": self.entry_ship_broker_email,
                "quantity": self.entry_quantity,
                "selling_price": self.entry_selling_price,
                "total_cost": self.entry_total_cost,
            }
            if not self.validate_inputs(entries):
                return

            # Get sale details
            sale_details = {
                "Sale ID": str(uuid.uuid4()) if not self.current_sale_id else self.current_sale_id,
                "Date": self.entry_date.get(),
                "Invoice Number": self.entry_invoice_number.get(),
                "Product": self.entry_product.get(),
                "Quantity": self.entry_quantity.get(),
                "Load Port": self.entry_load_port.get(),
                "Destination": self.entry_destination.get(),
                "Selling Price": self.entry_selling_price.get(),
                "Total Cost": self.entry_total_cost.get(),
                "Farmer Name": self.entry_farmer_name.get(),
                "Farmer Email": self.entry_farmer_email.get(),
                "Storage Name": self.entry_storage_name.get(),
                "Storage Email": self.entry_storage_email.get(),
                "Buyer Name": self.entry_buyer_name.get(),
                "Buyer Email": self.entry_buyer_email.get(),
                "Logistics Company": self.entry_logistics_company.get(),
                "Logistics Email": self.entry_logistics_email.get(),
                "Multilog Company": self.entry_multilog_company.get(),
                "Multilog Email": self.entry_multilog_email.get(),
                "Freight Forwarder": self.entry_freight_forwarder.get(),
                "Freight Forwarder Email": self.entry_freight_forwarder_email.get(),
                "Commodity Broker": self.entry_commodity_broker.get(),
                "Commodity Broker Email": self.entry_commodity_broker_email.get(),
                "Ship Broker": self.entry_ship_broker.get(),
                "Ship Broker Email": self.entry_ship_broker_email.get(),
            }

            # Save sale details to Tryton database
            with Transaction().start('database_name', 0, readonly=False) as transaction:
                Sale = Pool().get('comerciointl_module.sale')
                sale = Sale(**sale_details)
                sale.save()
                transaction.commit()

            messagebox.showinfo("Success", "Sale executed and details saved to the database.")
            self.clear_fields()
            self.current_sale_id = None  # Reset current sale ID after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute sale: {e}")

    def clear_fields(self):
        """
        Clear all input fields after a sale is executed.
        """
        entries = {
            "date": self.entry_date,
            "invoice_number": self.entry_invoice_number,
            "product": self.entry_product,
            "quantity": self.entry_quantity,
            "load_port": self.entry_load_port,
            "destination": self.entry_destination,
            "selling_price": self.entry_selling_price,
            "total_cost": self.entry_total_cost,
            "farmer_name": self.entry_farmer_name,
            "farmer_email": self.entry_farmer_email,
            "storage_name": self.entry_storage_name,
            "storage_email": self.entry_storage_email,
            "buyer_name": self.entry_buyer_name,
            "buyer_email": self.entry_buyer_email,
            "logistics_company": self.entry_logistics_company,
            "logistics_email": self.entry_logistics_email,
            "multilog_company": self.entry_multilog_company,
            "multilog_email": self.entry_multilog_email,
            "freight_forwarder": self.entry_freight_forwarder,
            "freight_forwarder_email": self.entry_freight_forwarder_email,
            "commodity_broker": self.entry_commodity_broker,
            "commodity_broker_email": self.entry_commodity_broker_email,
            "ship_broker": self.entry_ship_broker,
            "ship_broker_email": self.entry_ship_broker_email,
        }
        for entry in entries.values():
            entry.delete(0, "end")

    def search_sales(self):
        """
        Search sales by Sale ID, Date, or Buyer's Name using Tryton's backend.
        """
        sale_id = self.entry_search_sale_id.get()
        date = self.entry_search_date.get()
        buyer_name = self.entry_search_buyer_name.get()

        try:
            with Transaction().start('database_name', 0, readonly=True) as transaction:
                Sale = Pool().get('comerciointl_module.sale')
                domain = []
                if sale_id:
                    domain.append(('id', '=', sale_id))
                if date:
                    domain.append(('date', '=', date))
                if buyer_name:
                    domain.append(('buyer_name', 'ilike', f'%{buyer_name}%'))
                results = Sale.search(domain)

            if not results:
                messagebox.showinfo("Search Results", "No matching sales found.")
            else:
                self.display_search_results(results)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search sales: {e}")

    def display_search_results(self, results):
        """
        Display search results in a new window with a table.

        Args:
            results (list): List of dictionaries containing sale details.
        """
        result_window = tk.Toplevel(self.root)
        result_window.title("Search Results")

        # Create a Treeview widget
        columns = ["Sale ID", "Date", "Buyer Name", "Product", "Quantity", "Total Cost"]
        tree = ttk.Treeview(result_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insert data into the Treeview
        for row in results:
            tree.insert("", "end", values=[row[col] for col in columns])

        tree.pack(fill="both", expand=True)

    def upload_documents(self):
        """
        Upload documents related to the sale.
        """
        # Implement document upload logic here
        pass

    def validate_inputs(self, entries):
        """
        Validate critical inputs like email and numeric fields.

        Args:
            entries (dict): Dictionary of input fields to validate.

        Returns:
            bool: True if all inputs are valid, False otherwise.
        """
        try:
            # Validate emails
            emails = [
                entries["farmer_email"].get(),
                entries["storage_email"].get(),
                entries["buyer_email"].get(),
                entries["logistics_email"].get(),
                entries["multilog_email"].get(),
                entries["freight_forwarder_email"].get(),
                entries["commodity_broker_email"].get(),
                entries["ship_broker_email"].get(),
            ]
            for email in emails:
                if email and not self.validate_email(email):
                    messagebox.showwarning("Invalid Email", f"Invalid email format: {email}")
                    return False

            # Validate numeric fields
            quantity = entries["quantity"].get()
            selling_price = entries["selling_price"].get()
            total_cost = entries["total_cost"].get()
            if not quantity.isdigit() or not selling_price.replace(".", "").isdigit() or not total_cost.replace(".", "").isdigit():
                messagebox.showwarning("Invalid Input", "Quantity, Selling Price, and Total Cost must be numeric.")
                return False

            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error validating inputs: {e}")
            return False

    def validate_email(self, email):
        """
        Validate an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
