
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.price_total', 'payment_method_id')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            stamp_duty_tax = 0.0
            if order.payment_method_id:
            #     stamp_duty_config_id = order.payment_method_id.stamp_duty_config_id
            #     percentage = stamp_duty_config_id.tax_percentage or 0.0
            #     if percentage:
            #         if stamp_duty_config_id.is_include_tax:
            #             total = amount_tax + amount_untaxed
            #             stamp_duty_tax = (total * percentage) / 100
            #         else:
            #             stamp_duty_tax = (amount_untaxed * percentage) / 100
                total = amount_untaxed + amount_tax 
                if total < 10000:
                    stamp_duty_tax = 0
                elif total > 10000 and total < 250000:
                    stamp_duty_tax = total / 100
                elif total > 250000:
                    stamp_duty_tax = 2500
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax + stamp_duty_tax,
                'stamp_duty_tax': stamp_duty_tax,
            })

    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', domain=[('journal_id.type', '=', 'cash')])
    stamp_duty_tax = fields.Monetary(string='Stamp Duty', store=True, readonly=True, compute='_amount_all')

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['payment_method_id'] = self.payment_method_id.id
        return invoice_vals