# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class MOQwebsite(models.Model):
    _name = 'sh.moq.multi.website'
    _description = 'MOQ Multi Website'

    product_id = fields.Many2one('product.template', string="Product")
    website_id = fields.Many2one('website', string="Website")
    sh_increment_qty = fields.Char('Multiples of Quantity', default='1')
    sh_multiples_qty = fields.Char('Multiples of Quantitys', default='1')
