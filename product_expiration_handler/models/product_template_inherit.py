from odoo import api, fields, models

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    purchase_order_lines = fields.One2many(
        'purchase.order.line', 'product_template_id',
        string='Purchase Order Lines'
    )

    # Adjust the related field logic based on your requirements
    purchased_expiration_time = fields.Selection(
        related='purchase_order_lines.purchased_expiration_time',
        string='Product Expiration Time',
        readonly=True,
        store=True,
    )
