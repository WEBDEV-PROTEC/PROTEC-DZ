# -*- coding: utf-8 -*-

from odoo import models, fields, api


 
class webdescription(models.Model):
    _inherit = 'product.template'
    
    download_links = fields.Text(string='Lien PDF')
    
    
    
    @api.onchange('website_description')
    def _onchange_webdescription(self):
        aa = self.website_description.strip('<p>').strip('</').split('\n')
        for elt in aa:
            aa[aa.index(elt)] = "<p>" + elt + "</p>"
            
        self.website_description  = "".join(aa)
    