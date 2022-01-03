# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class Website(models.Model):
    _inherit = 'website'
    
    category_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3'),('style4','Style 4')], string="Category Style")
    category_header_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3')], string="Category Header Style")
    sub_category_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3'),('style4','Style 4')], string="Subcategory Style")       
        
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    category_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3'),('style4','Style 4')] ,related="website_id.category_style",string="Category Style",readonly=False)
    category_header_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3')],default='style1',related="website_id.category_header_style",string="Category Header Style",readonly=False)

    sub_category_style = fields.Selection( [('style1','Style 1'),('style2','Style 2'),('style3','Style 3'),('style4','Style 4')] ,related="website_id.sub_category_style",string="Subcategory Style",readonly=False)