from trytond.pool import Pool
from trytond.transaction import Transaction

class SearchHandler:
    def __init__(self, sales_dir="sales"):
        """
        Initialize the SearchHandler class.

        Args:
            sales_dir (str): Directory where sales records are stored.
        """
        self.sales_dir = sales_dir
        os.makedirs(self.sales_dir, exist_ok=True)

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
                return results
        except Exception as e:
            print(f"Error searching sales: {e}")
            return []