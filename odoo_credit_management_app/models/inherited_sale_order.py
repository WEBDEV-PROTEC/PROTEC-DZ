# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InheritedSaleOrder(models.Model):
    _inherit = 'sale.order'

    over_credit = fields.Boolean(string='Over Credit', tracking=True, copy=False)
    has_overdue = fields.Boolean(string='Override Credit Limit', tracking=True, copy=False)
    hold_delivery = fields.Boolean(string='Hold Delivery Till Payment', tracking=True,
                                   related='partner_id.hold_delivery', store=True)

    def action_confirm(self):
        for rec in self:
            if not rec.has_overdue:
                if (
                        rec.partner_id.credit_limit - rec.partner_id.total_credit_used + rec.partner_id.override_credit) < rec.amount_total:
                    raise ValidationError(_("Credit Limit Over \nCredit Limit:%d \nTotal Credit Used:%d \nTotal "
                                            "This "
                                            "Order:%d", ) % (
                                              rec.partner_id.credit_limit, rec.partner_id.total_credit_used,
                                              rec.amount_total))
            else:
                rec.over_credit = True
            if rec.partner_id:
                if rec.partner_id.credit_hold:
                    raise ValidationError(_("Credit Hold \nThis Customer is Hold"), )
                if rec.hold_delivery:
                    raise ValidationError(_("Delivery Hold \nThis Customer is Hold Delivery"), )
            rec.partner_id.total_credit_used += rec.amount_total

        return super(InheritedSaleOrder, self).action_confirm()

    def action_cancel(self):
        for rec in self:
            rec.partner_id.total_credit_used -= rec.amount_total
            rec.over_credit = False
            rec.has_overdue = False
        return super(InheritedSaleOrder, self).action_cancel()

    @api.onchange('partner_id')
    def onchange_partner_id_for_validation(self):
        for rec in self:
            if rec.partner_id:
                if rec.partner_id.credit_hold:
                    raise ValidationError(_("Credit Hold \nThis Customer is Hold"), )


class InheritedAccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        for rec in self:
            if rec.payment_type == 'inbound':
                rec.partner_id.total_credit_used -= rec.amount
        return super(InheritedAccountPayment, self).action_post()

    def action_draft(self):
        for rec in self:
            if rec.payment_type == 'inbound':
                rec.partner_id.total_credit_used += rec.amount
        return super(InheritedAccountPayment, self).action_draft()
