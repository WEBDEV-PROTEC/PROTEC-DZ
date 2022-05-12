# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
import logging

class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    equation_montant = fields.Text(string="Montant en lettre")

    
    