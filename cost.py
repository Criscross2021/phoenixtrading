from trytond.model import ModelSQL, ModelView, fields

class CostBreakdown(ModelSQL, ModelView):
    "Cost Breakdown"
    __name__ = 'comerciointl_module.cost_breakdown'

    sale = fields.Many2One('comerciointl_module.sale', 'Sale', required=True)
    cost_component = fields.Char('Cost Component', required=True)
    amount = fields.Float('Amount', required=True)
    currency = fields.Selection([
        ('USD', 'USD'),
        ('BRL', 'BRL'),
        ('EUR', 'EUR'),
        ('CNY', 'CNY'),
    ], 'Currency', required=True)

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._order = [('cost_component', 'ASC')]