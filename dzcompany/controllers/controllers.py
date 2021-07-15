# -*- coding: utf-8 -*-
# from odoo import http


# class Dzcompany(http.Controller):
#     @http.route('/dzcompany/dzcompany/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dzcompany/dzcompany/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dzcompany.listing', {
#             'root': '/dzcompany/dzcompany',
#             'objects': http.request.env['dzcompany.dzcompany'].search([]),
#         })

#     @http.route('/dzcompany/dzcompany/objects/<model("dzcompany.dzcompany"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dzcompany.object', {
#             'object': obj
#         })
