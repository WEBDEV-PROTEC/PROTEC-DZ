# -*- coding: utf-8 -*-

from odoo import models, fields, api


class contact_sequence(models.Model):

    _inherit = 'res.partner'
    ref = fields.Char(
        string="Code Client", readonly=True,
        required=True, copy=False, default='New')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=62)
   
    
    company_statut = fields.Selection([('eurl', 'EURL'),('sarl', 'SARL'),('snc', 'SNC'), ('spa', 'SPA'),('ets', 'ETS'),('epe', 'EPE'),('autre', 'Autre')], string='Type Société')
    
    num_rc = fields.Char(string="Num RC")
    art = fields.Char(string="ART")
    agrem = fields.Char(string="Num Agrement")
    exp_agrem = fields.Date(string="Date Expiration")
    #nouveau essai
    
   

    @api.model
    def create(self, vals):
        """ function for sequence creation"""
        type = vals.get('company_type')
        parent = vals.get('parent_id')
        if vals.get('ref', 'Non Défini') == 'Non Défini' and type =='company':
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'customer.sequence.company') or 'Non Défini'
        elif vals.get('ref', 'Non Défini') == 'Non Défini' and type =='person' and parent==0:
            
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'customer.sequence.individual') or 'Non Défini'
            
        result = super(contact_sequence, self).create(vals)
        return result
    #
    def write(self, vals):
        # """ function for sequence edit"""
        type = vals.get('company_type')
        parent = vals.get('parent_id')
        if type == 'company':
             vals['ref'] = self.self.env['ir.sequence'].next_by_code(
                'customer.sequence.company') or 'Non Défini'
        if type == 'person' :
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'customer.sequence.individual') or 'Non Défini'
        result = super(contact_sequence, self).write(vals)
        return result
    
    
    def unlink(self):
        
   
        for compa in self:
        
            if compa.company_type == 'company':
                current = self.env['ir.sequence'].search([('id','=',23)]).number_next_actual
                self.env['ir.sequence'].search([('id','=',23)]).update({'number_next_actual' : current-1 })
                self.env.cr.commit()
            if compa.company_type == 'person':
                current = self.env['ir.sequence'].search([('id','=',24)]).number_next_actual
                self.env['ir.sequence'].search([('id','=',24)]).update({'number_next_actual' : current-1})
                self.env.cr.commit()
            
        result = super(contact_sequence, self).unlink()
        return result

