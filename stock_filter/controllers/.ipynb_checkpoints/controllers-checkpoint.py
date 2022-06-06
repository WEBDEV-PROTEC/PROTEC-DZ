# -*- coding: utf-8 -*-
# from odoo import http

import hashlib
import json
from odoo import models, fields, api

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.osv import expression


class WebsiteSale(WebsiteSale):
    def _get_search_domain(self, search, category, attrib_values, search_in_description=True, search_in_brand=True):
            domains = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values, search_in_description)
        
            # In Stock
            in_stock = request.httprequest.args.get('in_stock')

            if in_stock=="1":

                domains = expression.AND([domains, [('qty_available', '>', 0)]])
            print(domains)
            return domains


    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(WebsiteSale, self).shop(page, category, search, ppg, **post)

        return response

# class StockFilter(http.Controller):
#     @http.route('/stock_filter/stock_filter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_filter/stock_filter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_filter.listing', {
#             'root': '/stock_filter/stock_filter',
#             'objects': http.request.env['stock_filter.stock_filter'].search([]),
#         })

#     @http.route('/stock_filter/stock_filter/objects/<model("stock_filter.stock_filter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_filter.object', {
#             'object': obj
#         })
