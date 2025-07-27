from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    last_checked_price = fields.Float("Last Checked Price", default=0.0)

    @api.model
    def send_email_cron(self):
        changed_products = self.search([
            ('list_price', '!=', 'last_checked_price')
        ])

        if not changed_products:
            _logger.info("No product price changes detected.")
            return

        template = self.env.ref('product_price_alert.email_template_price_change_report')

        if template:
            dummy = changed_products[0]
            ctx = {'products': changed_products, 'changed_count': len(changed_products)}
            template.with_context(ctx).send_mail(dummy.id, force_send=True)
            _logger.info("Product price change email sent for %s products", len(changed_products))

            # Update old prices
            for product in changed_products:
                product.last_checked_price = product.list_price
