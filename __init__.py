from trytond.pool import Pool
from . import models

def register():
    Pool.register(
        models.TradeTerm,
        models.Sale,
        models.CostBreakdown,
        module='comerciointl_module', type_='model')