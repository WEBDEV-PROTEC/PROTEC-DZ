# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api
import math

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def onchange_pro_qty(self):
        if self and self.env.company.sh_enable_multiple_qty_in_Backend_sale_order:
            for rec in self:
                multi_by = int(rec.product_id.sh_multiples_qty)
                if rec.product_uom_qty < multi_by:
                    rec.product_uom_qty = multi_by
                if rec.product_uom_qty > multi_by:
                    if multi_by != 0:
                        devi_value = rec.product_uom_qty/multi_by
                        ceil_value = math.ceil(devi_value)
                        rec.product_uom_qty = ceil_value * multi_by
