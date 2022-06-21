# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _


import logging

rec = 0
def autoIncrement():
    global rec
    pStart = 1
    pInterval = 1
    if rec == 0:
        rec = pStart
    else:
        rec += pInterval
    return rec

global_solde_total  = False
global_prev_context = {}
# hierarchy_account_ids = {}

class L10nAlgPlanComptable(models.TransientModel):
    _name = 'l10n_dz.plan_comptable'
    _description = 'Plan comptable Report'

    @api.model
    def get_journals(self):
        return [{'name': journal_id.name, 'id': journal_id.id} for journal_id in self.env['account.journal'].search([])]

    @api.model
    def get_exercices(self):
        return [{'name': exercice_id.name, 'id': exercice_id.id} for exercice_id in self.env['exercice'].search([])]

    @api.model
    def get_periodes1(self):
        return [{'name': period_id.name, 'id': period_id.id, 'exercice_id': period_id.exercice_id.id} for period_id in self.env['periode'].search([])]

    @api.model
    def get_periodes(self, exercice_id=False):
        context = dict(self.env.context)
        # exercice_id = context.get('selected_exercice')
        periodes = [{'name': '--', 'id': 0}]

        if exercice_id:
            periodes = periodes + [{'name': period_id.name, 'id': period_id.id} for period_id in self.env['periode'].search([('exercice_id','=',exercice_id)])]

        return periodes

    @api.model
    def _get_lines(self, line_id, line_ids, model, level):
        global global_solde_total
        context = dict(self.env.context)

        journal_id  = context.get('selected_journal')
        exercice_id = context.get('selected_exercice')
        period_id   = context.get('selected_periode')

        lines = []
        for line in line_ids:
            # recalcule du debit, credit selon les filtres
            if model == 'account.group':
                aa_ids = self.env['account.account'].search([('hierarchy_group_ids','=',line.id)])
            elif model == 'account.account':
                aa_ids = line

            aml_domain = [('account_id','in',aa_ids.ids)]
            if journal_id:
                aml_domain.append(('journal_id','=',journal_id))
            if exercice_id:
                aml_domain.append(('period_id.exercice_id','=',exercice_id))
            if period_id:
                aml_domain.append(('period_id','=',period_id))

            aml_ids = self.env['account.move.line'].search(aml_domain)
            debit   = sum(aml_ids.mapped('debit'))
            credit  = sum(aml_ids.mapped('credit'))

            dc_balance = round(debit, 5) - round(credit, 5)

            if line._name == 'account.group' and line.code_prefix_start == '0':
                global_solde_total = dc_balance

            lines.append({
                'id': autoIncrement(),
                'model': model,
                'model_id': line.id,
                'parent_id': line.parent_id.id if model == 'account.group' else line.group_id.id,
                'reference': line.name,
                'res_id': line.id,
                'res_model': model,
                'columns': [
                    line.code_prefix_start if model == 'account.group' else line.code,
                    line.name,
                    debit,
                    credit,
                    dc_balance,
                ],
                'level': level,
                'unfoldable': True if (model == 'account.group' and (line.group_ids or line.account_ids)) else False,
            })

        return lines

    @api.model
    def get_lines(self, line_id=None, **kw):
        global global_prev_context
        context = dict(self.env.context)

        model = kw and kw['model_name'] or context.get('model')
        rec_id = kw and kw['model_id'] or context.get('active_id')
        level = kw and kw['level'] or 1

        if not line_id:
            global_prev_context = context
            ag_ids = self.env['account.group'].search([], limit=1)
            aa_ids = []
        else:
            context = global_prev_context
            # reverifier line_id et context recu
            if line_id != kw.get('model_id'):
                line_id = self.env['account.group'].browse([kw.get('model_id')])
            else:
                line_id = self.env['account.group'].browse([line_id])

            ag_ids = line_id.group_ids
            aa_ids = line_id.account_ids

        return self.with_context(context)._get_lines(line_id, ag_ids, 'account.group', level) + \
               self.with_context(context)._get_lines(line_id, aa_ids, 'account.account', level)

    def _get_html(self):
        global global_solde_total

        result = {}
        rcontext = {}
        context = dict(self.env.context)
        rcontext['lines'] = self.with_context(context).get_lines()
        rcontext['solde_total'] = global_solde_total
        result['html'] = self.env.ref('eloapps_solde_compte.report_l10n_dz_html')._render(rcontext)

        return result

    @api.model
    def get_html(self, given_context=None):
        res = self.search([('create_uid', '=', self.env.uid)], limit=1)
        if not res:
            return self.create({}).with_context(given_context)._get_html()
        return res.with_context(given_context)._get_html()
