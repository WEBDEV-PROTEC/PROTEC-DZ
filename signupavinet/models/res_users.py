from odoo import api, fields, models

class ResUser(models.Model):
    _inherit = "res.users"


    token = fields.Char(string="Token")
