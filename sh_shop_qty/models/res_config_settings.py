# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models



class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_enable_multiple_qty_in_Backend_sale_order = fields.Boolean(string="Enable Multiples Qty In Backend Sale Order")

class Website(models.Model):
    _inherit = 'website'

    multi_website_moq = fields.Boolean("MOQ for Multi Website?", default=False)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    multi_website_moq = fields.Boolean(
        related="website_id.multi_website_moq", string="MOQ for Multi Website?", readonly=False)

    sh_enable_multiple_qty_in_Backend_sale_order = fields.Boolean(related="company_id.sh_enable_multiple_qty_in_Backend_sale_order",string="Enable Multiples Qty In Backend Sale Order",readonly=False)
