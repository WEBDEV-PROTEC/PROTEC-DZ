# -*- coding: utf-8 -*-
# from odoo import http


# class ProtecOptionalProducts(http.Controller):
#     @http.route('/protec_optional_products/protec_optional_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/protec_optional_products/protec_optional_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('protec_optional_products.listing', {
#             'root': '/protec_optional_products/protec_optional_products',
#             'objects': http.request.env['protec_optional_products.protec_optional_products'].search([]),
#         })

#     @http.route('/protec_optional_products/protec_optional_products/objects/<model("protec_optional_products.protec_optional_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('protec_optional_products.object', {
#             'object': obj
#         })
