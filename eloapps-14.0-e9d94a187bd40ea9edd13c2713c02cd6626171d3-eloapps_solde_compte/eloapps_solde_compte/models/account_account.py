# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging

class AccountAccount(models.Model):
    _inherit = 'account.account'

    hierarchy_group_ids = fields.Many2many(
        string='Hierarchie des groups',
        comodel_name='account.group',
    )

    def get_hierarchy_group_ids(self):
        curr_group_id = self.group_id
        group_ids = curr_group_id

        if curr_group_id:
            while curr_group_id and curr_group_id.code_prefix_start != '0':
                curr_group_id = curr_group_id.parent_id
                group_ids += curr_group_id

        return group_ids

    @api.constrains('group_id', 'group_id.parent_id', 'group_id.code_prefix_start')
    def constrains_hierarchy_group_ids(self):
        ag_id = self.env['account.group'].search([('code_prefix_start','=','0')])
        if ag_id and ag_id.group_ids:
            for aa_id in self:
                group_ids = aa_id.get_hierarchy_group_ids()
                aa_id.update({'hierarchy_group_ids': [(6, 0, group_ids.ids)]})

    @api.depends('move_line_ids', 'move_line_ids.debit', 'move_line_ids.credit')
    def _compute_debit_credit(self):
        for record in self:
            record.debit = sum(record.move_line_ids.mapped('debit'))
            record.credit = sum(record.move_line_ids.mapped('credit'))
            record.balance = record.debit - record.credit

            curr_group_id = record.group_id
            group_ids = [curr_group_id.id]

            while curr_group_id.parent_id:
                curr_group_id = curr_group_id.parent_id
                group_ids.append(curr_group_id.id)

            group_ids = self.env['account.group'].search([('id','in',group_ids)], order='id DESC')
            for group_id in group_ids:
                group_id._compute_debit_credit()

    debit = fields.Monetary(
        string="Debit",
        compute='_compute_debit_credit',
        store=True,
    )

    credit = fields.Monetary(
        string="Credit",
        compute='_compute_debit_credit',
        store=True,
    )

    balance = fields.Monetary(
        string="Balance",
        compute='_compute_debit_credit',
        store=True,
    )

    move_line_ids = fields.One2many(
        string='ecritures comptable',
        comodel_name='account.move.line',
        inverse_name='account_id',
    )

