# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
from odoo.exceptions import ValidationError
import logging as log

GLOBAL_REGEXEX_NIS_NIF = "^[a-zA-Z0-9]{15}$"
GLOBAL_REGEXEX_AI = "^[a-zA-Z0-9]{11}$"

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fiscal_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        string="Position fiscal"
    )

    rc = fields.Char(
        string="N° RC"
    )

    nis = fields.Char(
        string="N.I.S",
        size=15
    )

    ai = fields.Char(
        string="A.I",
        size=11
    )

    nif = fields.Char(
        string="N.I.F",
        size=15
    )

    fax = fields.Char(
        string="Fax",
        size=64
    )

    @api.constrains('nif')
    def is_valid_nif(self):
        for record in self:
            if record.nif:
                if not re.match(GLOBAL_REGEXEX_NIS_NIF, record.nif):
                    raise ValidationError("Veuillez verifier le N.I.F")

    @api.constrains('nis')
    def is_valid_nis(self):
        for record in self:
            if record.nis:
                if not re.match(GLOBAL_REGEXEX_NIS_NIF, record.nis):
                    raise ValidationError("Veuillez verifier le N.I.S")


    @api.constrains('ai')
    def is_valid_ai(self):
        for record in self:
            if record.ai:
                if not re.match(GLOBAL_REGEXEX_AI, record.ai):
                    raise ValidationError("Veuillez verifier le A.I")

    @api.model
    def _get_address_format(self):
        for record in self:
            format_adress = ""
            if record.state_id:
                format_adress = "%(street)s\n%(street2)s\n%(zip)s %(city)s (%(state_name)s), %(country_name)s"
            else:
                format_adress = "%(street)s\n%(street2)s\n%(zip)s %(city)s %(state_name)s %(country_name)s"
            return format_adress

class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{}".format(record.name)))
        return result