# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShProductTemplate(models.Model):
    _inherit = 'product.template'

    sh_increment_qty = fields.Char('Multiples of Quantity', default='1')
    sh_multiples_qty = fields.Char('Multiples of Quantitys', default='1')
    multi_website_ids = fields.One2many(
        'sh.moq.multi.website', 'product_id', string="Website wise MOQ")
    multi_website_moq = fields.Boolean(
         compute='_compute_multi_website_moq', 
         compute_sudo=True,
         string="MOQ for Multi Website?")

    def _compute_multi_website_moq(self):
        any_website_has_multi_website_moq = any(webiste.multi_website_moq for webiste in self.env['website'].search([]) )
        for product in self:
            product.multi_website_moq = any_website_has_multi_website_moq
