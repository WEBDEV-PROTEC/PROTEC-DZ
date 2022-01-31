# -*- coding: utf-8 -*-
# from odoo import http


# class Tags(http.Controller):
#     @http.route('/tags/tags/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tags/tags/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tags.listing', {
#             'root': '/tags/tags',
#             'objects': http.request.env['tags.tags'].search([]),
#         })

#     @http.route('/tags/tags/objects/<model("tags.tags"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tags.object', {
#             'object': obj
#         })
