# -*- coding: utf-8 -*-
# from odoo import http


# class ProductBannerA6(http.Controller):
#     @http.route('/product_banner_a6/product_banner_a6/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_banner_a6/product_banner_a6/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_banner_a6.listing', {
#             'root': '/product_banner_a6/product_banner_a6',
#             'objects': http.request.env['product_banner_a6.product_banner_a6'].search([]),
#         })

#     @http.route('/product_banner_a6/product_banner_a6/objects/<model("product_banner_a6.product_banner_a6"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_banner_a6.object', {
#             'object': obj
#         })
