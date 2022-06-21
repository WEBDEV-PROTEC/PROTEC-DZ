# -*- coding: utf-8 -*-
# from odoo import http


# class ImagesOrder(http.Controller):
#     @http.route('/images_order/images_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/images_order/images_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('images_order.listing', {
#             'root': '/images_order/images_order',
#             'objects': http.request.env['images_order.images_order'].search([]),
#         })

#     @http.route('/images_order/images_order/objects/<model("images_order.images_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('images_order.object', {
#             'object': obj
#         })
