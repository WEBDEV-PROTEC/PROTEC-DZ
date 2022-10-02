# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class product_banner_a6(models.Model):
#     _name = 'product_banner_a6.product_banner_a6'
#     _description = 'product_banner_a6.product_banner_a6'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
