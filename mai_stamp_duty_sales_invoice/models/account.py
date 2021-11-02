# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', copy=False)
    cash_ = fields.Boolean(sting = "Payment en liquide")
    stamp_duty_tax = fields.Monetary(string='Stamp Duty', store=True, readonly=True, compute='_compute_stamp_duty_tax')
    
    
    
    

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
        'payment_method_id',
        'invoice_line_ids',
        )
    def _compute_stamp_duty_tax(self):
        for move in self:
            stamp_duty_tax = 0.0
            if move.payment_method_id.journal_id.type == "cash":
                # stamp_duty_config_id = move.payment_method_id.stamp_duty_config_id
                # percentage = stamp_duty_config_id.tax_percentage or 0.0
                # if percentage:
                #     if stamp_duty_config_id.is_include_tax:
                #         total = move.amount_tax + move.amount_untaxed
                #         stamp_duty_tax = (total * percentage) / 100
                #     else:
                #         stamp_duty_tax = (move.amount_untaxed * percentage) / 100
                total = move.amount_tax + move.amount_untaxed
                if total < 10000:
                    stamp_duty_tax = 100
                elif total > 10000 and total < 250000:
                    stamp_duty_tax = total / 100
                elif total > 250000:
                    stamp_duty_tax = 2500
            move.stamp_duty_tax = stamp_duty_tax
            


    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
        'payment_method_id',
        'invoice_line_ids',
        'stamp_duty_tax'
        )
    def _compute_amount(self):
        for move in self:

            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id:
                    currencies.add(line.currency_id)

                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)

            stamp_duty_tax = 0.0
            if move.payment_method_id.journal_id.type == "cash":
                # stamp_duty_config_id = move.payment_method_id.stamp_duty_config_id
                # percentage = stamp_duty_config_id.tax_percentage or 0.0
                # if percentage:
                #     if stamp_duty_config_id.is_include_tax:
                #         total = move.amount_tax + move.amount_untaxed
                #         stamp_duty_tax = (total * percentage) / 100
                #     else:
                #         stamp_duty_tax = (move.amount_untaxed * percentage) / 100

                total = move.amount_tax + move.amount_untaxed
                if total < 10000:
                    stamp_duty_tax = 100
                elif total > 10000 and total < 250000:
                    stamp_duty_tax = total / 100
                elif total > 250000:
                    stamp_duty_tax = 2500

            amount_total = sign * (total_currency if len(currencies) == 1 else total)
            move.amount_total = amount_total + stamp_duty_tax
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
            move.amount_residual_signed = total_residual

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    if all(payment.is_matched for payment in move._get_reconciled_payments()):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state

    def create_update_stamp_duty_move_line(self):
        if self.payment_method_id.journal_id.type=="cash" and self.move_type == 'out_invoice':
            aml_obj =  self.env['account.move.line']
            name = self.payment_method_id.stamp_duty_config_id.name
            aml_stamp_duty_id = aml_obj.search([('move_id', '=', self.id), ('name', '=', name)])
            aml_debit_id = aml_obj.search([('move_id', '=', self.id), ('debit', '>', 0.0)], limit=1, order='id desc' )
            account_id = self.payment_method_id.stamp_duty_config_id.account_id.id
            
            if not aml_stamp_duty_id:
                self._cr.execute("""INSERT INTO account_move_line (
                    name, 
                    move_id, 
                    account_id, 
                    debit, 
                    credit, 
                    exclude_from_invoice_tab, 
                    currency_id, 
                    amount_currency, 
                    amount_residual_currency, 
                    company_currency_id,
                    balance
                    ) values 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                    (
                        name, 
                        self.id, 
                        account_id, 
                        0.0, 
                        self.stamp_duty_tax, 
                        True, 
                        self.currency_id.id,
                        -abs(self.stamp_duty_tax),
                        -abs(self.stamp_duty_tax), 
                        self.currency_id.id,
                        -abs(self.stamp_duty_tax), 
                        ))
            else:
                self._cr.execute("UPDATE account_move_line SET credit = '%s', amount_currency = '%s', balance = '%s' WHERE id='%s'" % (self.stamp_duty_tax, -abs(self.stamp_duty_tax),-abs(self.stamp_duty_tax), aml_stamp_duty_id.id))                
            self._cr.commit()
            # amount = sum(self.line_ids.mapped('credit'))
            amount = self.amount_residual
            try:
                self._cr.execute("UPDATE account_move_line SET debit = '%s', amount_currency = '%s', amount_residual= '%s', amount_residual_currency='%s', balance = '%s' WHERE id='%s'" % (amount, amount, amount, amount, amount, aml_debit_id.id))
            except:
                pass

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        res.create_update_stamp_duty_move_line()
        return res

    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        self.create_update_stamp_duty_move_line()
        return res
    
    
    
    
    @api.onchange('cash_')
    def _onchange_cash(self):
        if self.cash_ == True:
            cash_method = self.env['account.payment.method'].search([('code','=','Cash')])
            self.payment_method_id = cash_method
        else:
            self.payment_method_id = None 
            
            
            
            


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    journal_id = fields.Many2one('account.journal', 'Journal')
    stamp_duty_config_id = fields.Many2one('stamp.duty.config', 'Stamp Duty')
    payment_type = fields.Selection(default='inbound')


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def post(self):
        for rec in self:
            for invoice_id in rec.invoice_ids:
                if invoice_id.payment_method_id and invoice_id.payment_method_id.journal_id.type != self.journal_id.type:
                    raise UserError(_('Please select the Journal as a cash type because you have selected payment method type cash in invoice!'))
        return super(AccountPayment, self).post()


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"
   
    def action_create_payments(self):
        for rec in self:
            invoice_ids = self.env['account.move'].browse(self.env.context.get('active_id', False))
            for invoice_id in invoice_ids:
                if invoice_id.payment_method_id and invoice_id.payment_method_id.journal_id.type != self.journal_id.type:
                    raise UserError(_('Please select the Journal as a cash type because you have selected payment method type cash in invoice!'))
        res = super(AccountPaymentRegister, self).action_create_payments()
        return res
