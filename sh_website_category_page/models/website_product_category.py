# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import    api, fields,models

class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    show_category = fields.Boolean("Show Category ?",default=True)
    description = fields.Text("Description", translate=True)

    
