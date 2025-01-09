# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class sh_shop_qty_WebsiteSale(WebsiteSale):

    @http.route()
    def cart_update_json(self, *args, set_qty=None, **kwargs):

        if kwargs.get('product_id',False) and kwargs.get('add_qty',False):
            add_qty = kwargs.get('add_qty')
            
            if add_qty == 1:
                # First we check website wise multiple qty enabled or not 
                # if enabled then process that's way
                if  request.website.multi_website_moq:
                    product = request.env['product.product'].sudo().search([
                        ('id', '=', kwargs.get('product_id') )
                    ], limit = 1)
                    if product:
                        multiple_qty_lines = product.multi_website_ids.filtered(lambda line: line.website_id == request.website )
                        if multiple_qty_lines:
                            if multiple_qty_lines[0].sh_multiples_qty != add_qty:
                                kwargs['add_qty']  = multiple_qty_lines[0].sh_multiples_qty
                        else:
                            # if not any line found for website specifc then we picked quantity 
                            # from the product sh_multiples_qty field.
                            if product.sh_multiples_qty != add_qty:
                                kwargs['add_qty']  = product.sh_multiples_qty                       

                else:
                    # if setting for multipes of quantity not ticked.
                    # if website wise multiple qty not enabled then go with the product option
                    #  please pick multiple qty defined in product field.
                    product = request.env['product.product'].sudo().search([
                        ('id', '=', kwargs.get('product_id') )
                    ], limit = 1)
                    if product and product.sh_multiples_qty != add_qty:
                        kwargs['add_qty']  = product.sh_multiples_qty
        return super().cart_update_json(*args, set_qty=set_qty, **kwargs)
