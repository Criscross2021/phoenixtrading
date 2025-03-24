from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval

class Sale(ModelSQL, ModelView):
    "Sale"
    __name__ = 'comerciointl_module.sale'

    date = fields.Date('Date', required=True)
    invoice_number = fields.Char('Invoice Number', required=True)
    product = fields.Char('Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    buyer_name = fields.Char('Buyer Name', required=True)
    buyer_email = fields.Char('Buyer Email')
    total_cost = fields.Float('Total Cost', required=True)
    trade_term = fields.Many2One('comerciointl_module.trade_term', 'Trade Term', required=True)

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._order = [('date', 'DESC')]