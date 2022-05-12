# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import re
from odoo.exceptions import ValidationError

GLOBAL_REGEXEX_NIS_NIF = "^[a-zA-Z0-9]{15}$"

class ResCompany(models.Model):
    _inherit = 'res.company'

    fax = fields.Char(
        string="Fax",
        size=64
    )

    capital_social = fields.Float(
        string="Capital Social",
        digits=dp.get_precision('Account'),
        required=True,
        default=0.0
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

    forme_juridique = fields.Many2one(
        comodel_name='forme.juridique',
        string="Forme juridique"
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

class BaseDocumentLayout2(models.TransientModel):
    _inherit = 'base.document.layout'

    street = fields.Char(
        string=_('street'),
    )

    street2 = fields.Char(
        string=_('street2'),
    )

    zip = fields.Char(
        string=_('zip'),
    )

    city = fields.Char(
        string=_('city'),
    )

    state_id = fields.Many2one(
        'res.country.state',
        string=_('state'),
    )

    country_id = fields.Many2one(
        'res.country',
        string=_('country'),
    )
    
    
    fax = fields.Char(
        string="Fax",
        size=64
    )

    capital_social = fields.Float(
        string="Capital Social",
        digits=dp.get_precision('Account'),
        required=True,
        default=0.0
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

    forme_juridique = fields.Many2one(
        comodel_name='forme.juridique',
        string="Forme juridique"
    )
