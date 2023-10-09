# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InheritedStockPicking(models.Model):
    _inherit = 'stock.picking'

    over_credit = fields.Boolean(string='Over Credit', tracking=True, copy=False)
    has_overdue = fields.Boolean(string='Override Credit Limit', tracking=True, copy=False)

    def action_confirm(self):
        for rec in self:
            if rec.partner_id:
                if rec.partner_id.credit_hold:
                    raise ValidationError(_("Credit Hold \nThis Customer is Hold"), )

        return super(InheritedStockPicking, self).action_confirm()

    def action_assign(self):
        for rec in self:
            if rec.partner_id:
                if rec.partner_id.credit_hold:
                    raise ValidationError(_("Credit Hold \nThis Customer is Hold"), )

        return super(InheritedStockPicking, self).action_assign()

    def button_validate(self):
        for rec in self:
            if rec.partner_id:
                if rec.partner_id.credit_hold:
                    raise ValidationError(_("Credit Hold \nThis Customer is Hold"), )

        return super(InheritedStockPicking, self).button_validate()


    # def action_cancel(self):
    #     for rec in self:
    #         rec.partner_id.total_credit_used -= rec.amount_total
    #     return super(InheritedSaleOrder, self).action_cancel()
    #
    # @api.onchange('partner_id')
    # def onchange_partner_id_for_validation(self):
    #     for rec in self:
    #         if rec.partner_id:
    #             if rec.partner_id.credit_hold:
    #                 raise ValidationError(_("Credit Hold \nThis Customer is Hold"), )
