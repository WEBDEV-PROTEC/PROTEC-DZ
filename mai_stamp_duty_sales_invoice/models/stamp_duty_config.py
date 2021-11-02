# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StampDutyConfig(models.Model):
    _name = 'stamp.duty.config'
    _description = "Stamp Duty Configuration"

    name = fields.Char('Name', required=True)
    tax_percentage = fields.Float('Tax(%)', required=True)
    account_id = fields.Many2one('account.account', required=True)
    is_include_tax = fields.Boolean('Include Tax?')