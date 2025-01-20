# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # Compute and add Timbre stamp fee to journal entries
    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        line_vals_list = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals)

        for payment in self:
            if payment.use_timbre and line_vals_list:
                payment_line_dict = line_vals_list[0]

                # Adjust debit or credit with Timbre fee
                if payment_line_dict['debit']:
                    payment_line_dict['debit'] += payment.droit_timbre
                elif payment_line_dict['credit']:
                    payment_line_dict['credit'] += payment.droit_timbre

                company_currency = payment.company_id.currency_id
                if payment.currency_id == company_currency:
                    currency_id = False
                else:
                    amount_currency_timbre = payment.currency_id._convert(
                        payment.droit_timbre, company_currency, payment.company_id, payment.payment_date)
                    currency_id = payment.currency_id.id

                # Fetch Timbre account
                account_timbre_id = self.env['config.timbre'].search([], limit=1).sale_timbre
                if not account_timbre_id:
                    raise UserError(_('Please configure Timbre accounts under the Timbre settings.'))

                # Add Timbre move line
                line_vals_list.append({
                    'name': _('Timbre Fee'),
                    'amount_currency': amount_currency_timbre if currency_id else 0.0,
                    'currency_id': currency_id,
                    'debit': payment.droit_timbre if payment.payment_type == 'outbound' else 0.0,
                    'credit': payment.droit_timbre if payment.payment_type == 'inbound' else 0.0,
                    'date_maturity': payment.date,
                    'partner_id': payment.partner_id.id,
                    'account_id': account_timbre_id.id,
                    'payment_id': payment.id,
                })

        return line_vals_list

    # Synchronize payment changes to move lines
    def _synchronize_to_moves(self, changed_fields):
        if self._context.get('skip_account_move_synchronization'):
            return

        if not any(field_name in changed_fields for field_name in (
            'date', 'amount', 'payment_type', 'partner_type', 'payment_reference', 'currency_id',
            'partner_id', 'journal_id')):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):
            liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

            if pay.use_timbre:
                pay.droit_timbre = int(self.env['config.timbre']._timbre(pay.amount))

                # Update move lines with Timbre fee
                line_vals_list = pay._prepare_move_line_default_vals()
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                ]

                if pay.droit_timbre > 0.0:
                    line_ids_commands.append((0, 0, line_vals_list[2]))

                self.move_id.write({
                    'partner_id': pay.partner_id.id,
                    'currency_id': pay.currency_id.id,
                    'line_ids': line_ids_commands,
                })

                return

        super(AccountPayment, self)._synchronize_to_moves(changed_fields)

    # Determine if Timbre calculation applies
    @api.depends('journal_id')
    def _visible_timbre(self):
        for payment in self:
            payment.use_timbre = payment.journal_id.type == 'cash'

    # Calculate Timbre fee
    @api.depends('amount', 'use_timbre')
    def _calcule_timbre(self):
        for payment in self:
            if payment.use_timbre:
                payment.droit_timbre = int(self.env['config.timbre']._timbre(payment.amount))

    use_timbre = fields.Boolean(
        string='Apply Timbre Fee',
        compute='_visible_timbre',
        store=True,
    )

    droit_timbre = fields.Monetary(
        string='Timbre Fee',
        compute='_calcule_timbre',
        store=True,
    )


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    # Add Timbre fee to payment values
    def _create_payment_vals_from_wizard(self):
        result = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        result['droit_timbre'] = self.droit_timbre
        return result

    # Determine if Timbre calculation applies
    @api.depends('journal_id')
    def _visible_timbre(self):
        for payment in self:
            payment.use_timbre = payment.journal_id.type == 'cash'

    # Calculate Timbre fee
    @api.depends('amount', 'use_timbre')
    def _calcule_timbre(self):
        for payment in self:
            if payment.use_timbre:
                payment.droit_timbre = int(self.env['config.timbre']._timbre(payment.amount))
                payment.montant_avec_timbre = payment.amount + payment.droit_timbre

    use_timbre = fields.Boolean(
        string='Apply Timbre Fee',
        compute='_visible_timbre',
        store=True,
    )

    droit_timbre = fields.Monetary(
        string='Timbre Fee',
        compute='_calcule_timbre',
        store=True,
    )

    montant_avec_timbre = fields.Monetary(
        string='Total with Timbre',
        compute='_calcule_timbre',
        store=True,
    )


class PaymentMode(models.Model):
    _name = 'account.payment.mode'

    name = fields.Char(
        string="Name",
        required=True,
    )

    mode_type = fields.Selection(
        [('cash', 'Cash'),
         ('bank', 'Bank'),
         ('other', 'Other')],
        string="Type",
    )
