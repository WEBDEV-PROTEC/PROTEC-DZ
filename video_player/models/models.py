# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class video_player(models.Model):
#     _name = 'video_player.video_player'
#     _description = 'video_player.video_player'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
