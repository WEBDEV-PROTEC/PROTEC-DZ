from odoo import api, fields, models


class dr_product_tags(models.Model):
    _inherit = 'dr.product.tags'

    image = fields.Binary('Image')



#ajouter des images aux tags
#test