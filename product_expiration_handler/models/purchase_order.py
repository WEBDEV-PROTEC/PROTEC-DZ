from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    product_template_id = fields.Many2one(
    'product.template',
    string='Product Template',
    help='Link to the product template',
)
    purchased_expiration_time = fields.Selection([
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('9_months', '9 Months'),
        ('1_year', '1 Year'),
        ('3_year', '3 Year'),
        ('5_years', '5 Years'),
        ('10_years', '10 Years'),
    ], string='Expiration Time', help='Select the purchased expiration period')

    @api.model
    def create(self, values):
        order_line = super(PurchaseOrderLine, self).create(values)
        order_line.enable_tracking()
        return order_line

    def write(self, values):
        result = super(PurchaseOrderLine, self).write(values)
        self.enable_tracking()
        return result

    def enable_tracking(self):
        for line in self:
            if line.purchased_expiration_time:
                # Enable tracking for the related product
                line.product_id.product_tmpl_id.write({'tracking': 'serial'})
                
                # Set use_expiration_date to true
                line.product_id.product_tmpl_id.write({'use_expiration_date': True})
                
                # Set expiration_time based on the selected purchased_expiration_time
                expiration_times = {
                    '1_month': 30,
                    '3_months': 90,
                    '6_months': 180,
                    '9_months': 270,
                    '1_year': 365,
                    '3_years': 3 * 365,
                    '5_years': 5 * 365,
                    '10_years': 10 * 365,
                }
                line.product_id.product_tmpl_id.write({'expiration_time': expiration_times.get(line.purchased_expiration_time, 0)})
                
                # Set alert_time to expiration_time - 15
                alert_time = expiration_times.get(line.purchased_expiration_time, 0) - 15
                line.product_id.product_tmpl_id.write({'alert_time': alert_time})
