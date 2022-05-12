# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FormeJuridique(models.Model):
    _name = 'forme.juridique'

    name = fields.Char(
        string="Nom",
        required=True
    )

    code = fields.Char(
        string="Code"
    )