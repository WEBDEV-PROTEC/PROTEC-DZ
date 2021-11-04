# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class src/user/protec_partners(models.Model):
#     _name = 'src/user/protec_partners.src/user/protec_partners'
#     _description = 'src/user/protec_partners.src/user/protec_partners'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
