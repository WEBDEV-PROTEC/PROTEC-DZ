from odoo import models, api


class CustomReportProductPricelist(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'

    @api.model
    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        data = super(CustomReportProductPricelist, self)._get_product_data(is_product_tmpl, product, pricelist, quantities)
        data.update({
            'image_128': product.image_128,  # Add image field
            'default_code': product.default_code,  # Add default code field
        })
        return data