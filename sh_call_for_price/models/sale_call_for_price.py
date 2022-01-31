# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class SaleCallForPrice(models.Model):
    _name = 'sale.call.for.price'
    _description = 'Call For Price'

    name = fields.Many2one("product.product", "Product", required=True)
    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    email = fields.Char("Email")
    contact_no = fields.Char("Contact No.")
    quantity = fields.Float("Quantity")
    message = fields.Text("Message")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),
                              ('cancel', 'Cancel')], default='draft', readonly=True, index=True)

    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    call_for_price = fields.Boolean("Call For Price ?")
