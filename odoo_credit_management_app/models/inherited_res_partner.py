from datetime import datetime, date

from odoo import api, fields, models


class InheritedResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(string='Credit Limit', tracking=True)
    total_credit_used = fields.Float(string='Used Credit', tracking=True)
    credit_hold = fields.Boolean(string='Credit Hold', tracking=True)
    has_overdue = fields.Boolean(string='Has Overdue  Invoice', tracking=True, compute='_compute_has_overdue',
                                 default=False,
                                 )
    override_credit = fields.Float(string='Override Credit Threshold', tracking=True)
    hold_delivery = fields.Boolean(string='Hold Delivery Till Payment', tracking=True)

    # @api.depends('invoice_ids', 'invoice_ids.payment_state','invoice_ids.payment_id', 'invoice_ids.invoice_date',
    #              'invoice_ids.invoice_date_due', 'invoice_ids.invoice_payment_term_id','total_invoiced','invoice_ids.state',)
    def _compute_has_overdue(self):
        invoice_obj = self.env['account.move']
        for rec in self:
            has_overdue = False
            invoice_ids = invoice_obj.search([('partner_id', '=', rec.id), ('payment_state', '!=', 'paid')])
            for invoice_id in invoice_ids:
                print("INVOICE", invoice_id.invoice_date)
                if invoice_id.invoice_date_due:
                    print("HIIIII")
                    if invoice_id.invoice_date_due < date.today():
                        print("hELLLLLOOO")
                        has_overdue = True
                        break
            if has_overdue:
                rec.has_overdue = True
            else:
                rec.has_overdue = False
