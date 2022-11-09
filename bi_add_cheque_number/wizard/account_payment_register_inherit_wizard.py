# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = "account.payment.register"
    _description = "Payments Register"

    cheq_num = fields.Char(string="N° de Chèque")
    cheq_img = fields.Binary(string="Image")
    cheq_bank = fields.Char(string="Etabliessement payeur")
    cheq_place = fields.Char(string="Lieu de paiement")
    cheq_name = fields.Char(string="Nom du tireur")

    def _create_payments(self) :
        res = super(AccountPaymentRegisterInherit,self)._create_payments()
        res.write({"cheq_num" : self.cheq_num, "cheq_img" : self.cheq_img, "cheq_bank" : self.cheq_bank, "cheq_place" : self.cheq_place, "cheq_name" : self.cheq_name,})
        return res