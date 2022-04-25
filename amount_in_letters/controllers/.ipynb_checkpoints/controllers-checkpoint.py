# -*- coding: utf-8 -*-
# from odoo import http


# class AmountInLetters(http.Controller):
#     @http.route('/amount_in_letters/amount_in_letters/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/amount_in_letters/amount_in_letters/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('amount_in_letters.listing', {
#             'root': '/amount_in_letters/amount_in_letters',
#             'objects': http.request.env['amount_in_letters.amount_in_letters'].search([]),
#         })

#     @http.route('/amount_in_letters/amount_in_letters/objects/<model("amount_in_letters.amount_in_letters"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('amount_in_letters.object', {
#             'object': obj
#         })
