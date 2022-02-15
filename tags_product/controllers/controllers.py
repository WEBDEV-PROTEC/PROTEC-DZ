# -*- coding: utf-8 -*-
# from odoo import http


# class TagsProduct(http.Controller):
#     @http.route('/tags_product/tags_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tags_product/tags_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tags_product.listing', {
#             'root': '/tags_product/tags_product',
#             'objects': http.request.env['tags_product.tags_product'].search([]),
#         })

#     @http.route('/tags_product/tags_product/objects/<model("tags_product.tags_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tags_product.object', {
#             'object': obj
#         })
