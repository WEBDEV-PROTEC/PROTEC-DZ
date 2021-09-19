# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class order_amount_letters(models.Model):
    _inherit = 'sale.order'
    
    
    price_letters = fields.Char(
    string='la somme totale en lettres',
    compute='_compute_orderprice_letters',
    store=True, # optional
    compute_sudo=True # optional
    )
    
    
    @api.depends('amount_total')
    def _compute_orderprice_letters(self):
        for order in self:
            order.price_letters = num2words(order.amount_total, lang='fr').title()+ " Dinar Algérien"

            
            
