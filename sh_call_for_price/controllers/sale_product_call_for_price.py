# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.http import request


class SaleProductCallForPrice(http.Controller):

    @http.route(['/sale/product_call_for_price'], type='json', auth="public", methods=['POST'], website=True)
    def sale_product_call_for_price(self, **post):

        if post.get('product_id', False):

            product_search = request.env['product.product'].sudo().search(
                [('id', '=', post.get('product_id'))], limit=1)

            if product_search:

                vals = {'name': product_search.id}

                if post.get('first_name', False):
                    vals.update({'first_name': post.get('first_name')})

                if post.get('last_name', False):
                    vals.update({'last_name': post.get('last_name')})

                if post.get('email', False):
                    vals.update({'email': post.get('email')})

                if post.get('contact_no', False):
                    vals.update({'contact_no': post.get('contact_no')})

                if post.get('quantity', False):
                    vals.update({'quantity': post.get('quantity')})

                if post.get('message', False):
                    vals.update({'message': post.get('message')})

                call_price_obj = request.env['sale.call.for.price'].sudo().create(
                    vals)

                if call_price_obj:
                    return 1
        return 0
