# -*- coding: utf-8 -*-

from odoo import models, fields, api

class batch_payment_pdf(models.Model):
    _inherit= "account.batch.payment"

    def custom_amount_to_text(self, montant):
        currency_id = self.currency_id or self.env.ref('base.DZD')
        res = currency_id.amount_to_text(montant)
        if round(montant % 1, 2) == 0.0:
            res += " et zéro centime"
        if montant > 1.0:
            res = res.replace('Dinar', 'Dinars')
        return res.lower().capitalize()