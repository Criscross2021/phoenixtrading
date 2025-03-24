import os
import shutil
from tkinter import filedialog
from trytond.pool import Pool
from trytond.transaction import Transaction

class DocumentHandler:
    def __init__(self, upload_dir="uploads"):
        """
        Initialize the DocumentHandler class.

        Args:
            upload_dir (str): Directory to store uploaded documents.
        """
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def upload_documents(self, sale_id=None):
        """
        Upload documents and save metadata to the Tryton database.

        Args:
            sale_id (str): Sale ID to associate with the uploaded documents.

        Returns:
            list: List of paths to the uploaded documents.
        """
        file_paths = filedialog.askopenfilenames(title="Select Documents", filetypes=[("All Files", "*.*")])
        if not file_paths:
            return []

        try:
            with Transaction().start('database_name', 0, readonly=False) as transaction:
                Document = Pool().get('comerciointl_module.document')
                for file_path in file_paths:
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(self.upload_dir, file_name)
                    shutil.copy(file_path, destination_path)

                    # Save document metadata to Tryton database
                    document = Document(
                        sale_id=sale_id,
                        file_path=destination_path,
                    )
                    document.save()
                transaction.commit()
                return file_paths
        except Exception as e:
            print(f"Error uploading documents: {e}")
            return []