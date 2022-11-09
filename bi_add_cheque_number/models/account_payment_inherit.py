# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AccountPaymentInherit(models.Model) :
    _inherit = "account.payment"
    _description = "Payments"

    cheq_num = fields.Char(string="N° de Chèque")
    cheq_img = fields.Binary(string="Image")
    cheq_bank = fields.Char(string="Etabliessement payeur")
    cheq_place = fields.Char(string="Lieu de paiement")
    cheq_name = fields.Char(string="Nom du tireur")