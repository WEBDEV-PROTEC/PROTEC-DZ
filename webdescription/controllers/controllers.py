# -*- coding: utf-8 -*-
# from odoo import http


# class Webdescription(http.Controller):
#     @http.route('/webdescription/webdescription/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/webdescription/webdescription/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('webdescription.listing', {
#             'root': '/webdescription/webdescription',
#             'objects': http.request.env['webdescription.webdescription'].search([]),
#         })

#     @http.route('/webdescription/webdescription/objects/<model("webdescription.webdescription"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('webdescription.object', {
#             'object': obj
#         })
