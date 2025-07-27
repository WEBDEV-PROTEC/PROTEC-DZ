# -*- coding: utf-8 -*-
# from odoo import http


# class PriceAlert(http.Controller):
#     @http.route('/price_alert/price_alert/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/price_alert/price_alert/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('price_alert.listing', {
#             'root': '/price_alert/price_alert',
#             'objects': http.request.env['price_alert.price_alert'].search([]),
#         })

#     @http.route('/price_alert/price_alert/objects/<model("price_alert.price_alert"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('price_alert.object', {
#             'object': obj
#         })
