

from odoo import api, models, fields


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    
    city = fields.Many2one('res.city', string='City')
    dzcompany_type = fields.Selection(
        [('Sarl', 'SARL'), ('Eurl', 'EURL'), ('Spa', 'SPA'), ('Snc', 'SNC')
         
         ], string='Forme juridique ')


    
    @api.onchange('city')
    def _onchange_city_id(self):
        if self.city:
            self.state_id = self.city.state_id
            self.zip = self.city.zipcode
            
            
    