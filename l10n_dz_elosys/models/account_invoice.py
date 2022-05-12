# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
import logging

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    montant_en_lettres = fields.Monetary( string="Montant calculé" ,compute="calcule_amount")

    equation_montant = fields.Text(string="Equation du montant", readonly="1", compute="compute_equation_montant")

    def compute_equation_montant(self):
        for record in self:
            record.equation_montant= record.journal_id.equation_montant


    
    def calcule_amount(self):
        for record in self:
            if record.equation_montant:
                localdict = {'result': None, 'invoice': record}


                safe_eval(self.equation_montant, localdict, mode='exec', nocopy=True)

                res = localdict['result']
                logging.warn(res)

                record.montant_en_lettres = res
            else :
                record.montant_en_lettres = record.amount_total




    def custom_amount_to_text(self, montant):
        currency_id = self.currency_id or self.env.ref('base.DZD')
        res = currency_id.amount_to_text(montant)
        if round(montant % 1, 2) == 0.0:
            res += " et zéro centime"
        if montant > 1.0:
            res = res.replace('Dinar', 'Dinars')
        return res.lower().capitalize()