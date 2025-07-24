# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class product_price_alert(models.Model):
#     _name = 'product_price_alert.product_price_alert'
#     _description = 'product_price_alert.product_price_alert'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
