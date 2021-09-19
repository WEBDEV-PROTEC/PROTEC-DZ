# -*- coding: utf-8 -*-
# from odoo import http


# class AmountLetters(http.Controller):
#     @http.route('/amount_letters/amount_letters/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/amount_letters/amount_letters/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('amount_letters.listing', {
#             'root': '/amount_letters/amount_letters',
#             'objects': http.request.env['amount_letters.amount_letters'].search([]),
#         })

#     @http.route('/amount_letters/amount_letters/objects/<model("amount_letters.amount_letters"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('amount_letters.object', {
#             'object': obj
#         })
