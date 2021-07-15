from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError, ValidationError
import pdb
import requests
import json

class ResPartner(models.Model):
    _inherit = "res.partner"

    dzcompany_type = fields.Selection(
        [('Sarl', 'SARL'), ('Eurl', 'EURL'), ('Spa', 'SPA'), ('Snc', 'SNC')
         
         ], string='Forme juridique ')

