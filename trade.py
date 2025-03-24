from trytond.model import ModelSQL, ModelView, fields

class TradeTerm(ModelSQL, ModelView):
    "Trade Term"
    __name__ = 'comerciointl_module.trade_term'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._order = [('name', 'ASC')]