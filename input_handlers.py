import re
import logging

# Configure logging
logging.basicConfig(filename="input_handler.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class InputHandler:
    def __init__(self):
        """
        Initialize the InputHandler class.
        """
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
                    logging.warning(f"Invalid email format: {email}")
                    return False

            # Validate numeric fields
            quantity = entries["quantity"].get()
            selling_price = entries["selling_price"].get()
            total_cost = entries["total_cost"].get()
            if not quantity.isdigit() or not selling_price.replace(".", "").isdigit() or not total_cost.replace(".", "").isdigit():
                logging.warning("Quantity, Selling Price, and Total Cost must be numeric.")
                return False

            return True
        except Exception as e:
            logging.error(f"Error in validate_inputs: {e}")
            return False

    def validate_email(self, email):
        """
        Validate an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def clear_fields(self, entries):
        """
        Clear all input fields.

        Args:
            entries (dict): Dictionary of input fields to clear.
        """
        try:
            for entry in entries.values():
                entry.delete(0, "end")
            logging.info("All input fields cleared.")
        except Exception as e:
            logging.error(f"Error clearing fields: {e}")