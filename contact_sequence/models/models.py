# -*- coding: utf-8 -*-

from odoo import models, fields, api


class contact_sequence(models.Model):

    _inherit = 'res.partner'

    code_client = fields.Char(
        string="Code Client",
        required=True, copy=False, default='New')
    num_rc = fields.Char(string="Num RC")
    vat = fields.Char(string="NIF")
    art = fields.Char(string="ART")
    @api.model
    def create(self, vals):
        """ function for sequence creation"""
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        current_code_file =  open("~/data/code_client.conf","r+")
        current_code =  current_code_file.readline()
        if int(current_code[1:])<=9999:
            seq = str(int('4' + current_code[1:] ) + 1)[1:]
            current_code = current_code[0]+seq
        else:
            current_code = letters[letters.index(current_code[0])+1]+'0001'
            with open("~/data/code_client.conf", 'w') as c:
                c.write(current_code)
                c.close()
            
        
           
        vals['code_client'] = current_code
        result = super(contact_sequence, self).create(vals)
        return result
    #
   #name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
