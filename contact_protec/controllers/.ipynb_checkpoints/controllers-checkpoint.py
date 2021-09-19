# -*- coding: utf-8 -*-
# from odoo import http


# class ContactProtec(http.Controller):
#     @http.route('/contact_protec/contact_protec/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contact_protec/contact_protec/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('contact_protec.listing', {
#             'root': '/contact_protec/contact_protec',
#             'objects': http.request.env['contact_protec.contact_protec'].search([]),
#         })

#     @http.route('/contact_protec/contact_protec/objects/<model("contact_protec.contact_protec"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contact_protec.object', {
#             'object': obj
#         })
