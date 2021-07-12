# -*- coding: utf-8 -*-
# from odoo import http


# class Citycontact(http.Controller):
#     @http.route('/citycontact/citycontact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/citycontact/citycontact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('citycontact.listing', {
#             'root': '/citycontact/citycontact',
#             'objects': http.request.env['citycontact.citycontact'].search([]),
#         })

#     @http.route('/citycontact/citycontact/objects/<model("citycontact.citycontact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('citycontact.object', {
#             'object': obj
#         })
