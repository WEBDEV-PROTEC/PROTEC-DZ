# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import logging
from odoo.tools import float_is_zero

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    payment_mode = fields.Many2one(
        'account.payment.mode',
        string="Mode de paiement",
    )

    amount_timbre = fields.Monetary(
        string='Droit de timbre',
        readonly=True,
        compute='_compute_amount_timbre'
    )

    total_timbre = fields.Monetary(
        string='Montant avec timbre',
        readonly=True,
        compute='_compute_amount_timbre'
    )

    payment_mode_type = fields.Char("Type")

    montant_en_lettre = fields.Boolean(
        string="Afficher le montant en lettre sur l’impression des factures",
        compute='get_timbre_montant_en_lettre',
    )

    @api.onchange('payment_mode')
    def _onchange_payment_mode(self):
        for record in self:
            record.payment_mode_type = record.payment_mode.mode_type if record.payment_mode else False

    def _timbre(self, amount_total):
        timbre = 0.0
        if self.payment_mode and self.payment_mode.mode_type == "cash":
            timbre = self.env['config.timbre']._timbre(amount_total)
        return timbre

    @api.depends('amount_total')
    def _compute_amount_timbre(self):
        for record in self:
            record.amount_timbre = int(record._timbre(record.amount_total))
            record.total_timbre = record.amount_total + record.amount_timbre if record.amount_timbre else 0.0

    @api.depends('payment_mode')
    def get_timbre_montant_en_lettre(self):
        for record in self:
            logic = False
            timbre = self.env['config.timbre'].search([],limit=1)
            if record.payment_mode and record.payment_mode.mode_type == "cash":
                logic = timbre.montant_en_lettre
            record.montant_en_lettre = logic
           
    def custom_amount_to_text(self, montant):
        currency_id = self.currency_id or self.env.ref('base.DZD')
        res = currency_id.amount_to_text(montant)
        if round(montant % 1, 2) == 0.0:
            res += " et zéro centime"
        if montant > 1.0:
            res = res.replace('Dinar', 'Dinars')
        return res.lower().capitalize()



        
