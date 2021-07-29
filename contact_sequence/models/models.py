# -*- coding: utf-8 -*-

from odoo import models, fields, api


class contact_sequence(models.Model):

    _inherit = 'res.partner'
    
 

    code_client = fields.Char(
        string="Code Client",
        readonly=True)
    num_rc = fields.Char(string="Num RC / AGREM")
    vat = fields.Char(string="NIF")
    art = fields.Char(string="ART")
    @api.model
    def create(self, vals):
        """ function for sequence creation"""
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        current_code_file =  open("/home/odoo/data/code_client.conf","r+")
        current_code =  current_code_file.readline()
        if int(current_code[1:])<9999:
            seq = str(int('4' + current_code[1:] ) + 1)[1:]
            current_code = current_code[0]+seq
        if int(current_code[1:])==9999:
            current_code = letters[letters.index(current_code[0])+1]+'0001'
            with open("/home/odoo/data/code_client.conf", 'w') as c:
                c.write(current_code)
                c.close()
            
        
           
        vals['code_client'] = current_code
        result = super(contact_sequence, self).create(vals)
        return result
    def unlink(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        with open("/home/odoo/data/code_client.conf", 'w') as c:
                current_code = self.code_client[1:]
                if current_code=='0001':
                    current_code = letters[letters.index(self.code_client[0])-1]+'9999'
                else:
                    current_code=self.code_client[0] + str(int('4' + current_code[1:] ) - 1)[1:]
                    
                    
                c.write(current_code)
                c.close()
    
        result = super(contact_sequence, self).unlink()
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
