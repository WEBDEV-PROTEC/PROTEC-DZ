# -*- coding: utf-8 -*-
# from odoo import http


# class ContactSequence(http.Controller):
#     @http.route('/contact_sequence/contact_sequence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contact_sequence/contact_sequence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('contact_sequence.listing', {
#             'root': '/contact_sequence/contact_sequence',
#             'objects': http.request.env['contact_sequence.contact_sequence'].search([]),
#         })

#     @http.route('/contact_sequence/contact_sequence/objects/<model("contact_sequence.contact_sequence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contact_sequence.object', {
#             'object': obj
#         })
