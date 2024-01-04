# inventory_changes.py
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        # Add change tracking value
        vals['tracking'] = 'serial'
        return super(ProductTemplate, self).create(vals)

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def _get_use_expiration_date(self, product):
        # Set use_expiration_date to true for items with expiration_time
        return bool(product.expiration_time)

    @api.model
    def _get_expiration_time_days(self, product):
        # Calculate expiration time in days
        if product.expiration_time:
            today_date = fields.Datetime.now()
            expiration_time = fields.Datetime.from_string(product.expiration_time)
            return (expiration_time - today_date).days
        return 0

    use_expiration_date = fields.Boolean(default=_get_use_expiration_date)
    expiration_time_days = fields.Integer(default=_get_expiration_time_days)
