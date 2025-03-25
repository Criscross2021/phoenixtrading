import csv
import os
import uuid
from datetime import datetime
import shutil
import logging

# Configure logging
logging.basicConfig(filename="file_handler.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FileHandler:
    def __init__(self, sales_dir="sales"):
        """
        Initialize the FileHandler class.

        Args:
            sales_dir (str): Directory to store sales records.
        """
        self.sales_dir = sales_dir
        os.makedirs(self.sales_dir, exist_ok=True)

    def save_sale(self, sale_details):
        """
        Save sale details to a CSV file.

        Args:
            sale_details (dict): Dictionary containing sale details.

        Returns:
            str: Path to the saved file.
        """
        try:
            # Generate file name
            file_name = f"{sale_details['Invoice Number']}_{sale_details['Date']}_{sale_details['Buyer Name']}.csv"
            file_path = os.path.join(self.sales_dir, file_name)

            # Check for duplicate invoice numbers
            if os.path.exists(file_path):
                logging.warning(f"Duplicate invoice number: {sale_details['Invoice Number']}")
                return None

            # Save sale details to CSV
            with open(file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=sale_details.keys())
                writer.writeheader()
                writer.writerow(sale_details)

            logging.info(f"Sale saved to {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Error saving sale: {e}")
            return None

    def search_sales(self, sale_id=None, date=None, buyer_name=None):
        """
        Search sales by Sale ID, Date, or Buyer's Name.

        Args:
            sale_id (str): Sale ID to search for.
            date (str): Date to search for.
            buyer_name (str): Buyer's name to search for.

        Returns:
            list: List of dictionaries containing matching sale details.
        """
        results = []
        try:
            for file_name in os.listdir(self.sales_dir):
                if file_name.endswith(".csv"):
                    with open(os.path.join(self.sales_dir, file_name), "r") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if (not sale_id or sale_id == row["Sale ID"]) and \
                               (not date or date == row["Date"]) and \
                               (not buyer_name or buyer_name.lower() in row["Buyer Name"].lower()):
                                results.append(row)
            logging.info(f"Found {len(results)} matching sales.")
        except Exception as e:
            logging.error(f"Error searching sales: {e}")
        return results

    def delete_sale(self, sale_id):
        """
        Delete a sale record by Sale ID.

        Args:
            sale_id (str): Sale ID to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            for file_name in os.listdir(self.sales_dir):
                if file_name.endswith(".csv"):
                    with open(os.path.join(self.sales_dir, file_name), "r") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if row["Sale ID"] == sale_id:
                                os.remove(os.path.join(self.sales_dir, file_name))
                                logging.info(f"Deleted sale: {file_name}")
                                return True
            logging.warning(f"No sale found with ID: {sale_id}")
            return False
        except Exception as e:
            logging.error(f"Error deleting sale: {e}")
            return False

    def create_backup(self, backup_dir="sales_backup"):
        """
        Create a backup of the sales directory.

        Args:
            backup_dir (str): Directory to store the backup.

        Returns:
            bool: True if backup was successful, False otherwise.
        """
        try:
            os.makedirs(backup_dir, exist_ok=True)
            shutil.copytree(self.sales_dir, os.path.join(backup_dir, os.path.basename(self.sales_dir)))
            logging.info(f"Backup created in {backup_dir}")
            return True
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            return False
