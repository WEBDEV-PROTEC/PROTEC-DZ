# -*- coding: utf-8 -*-
# from odoo import http


# class BatchPaymentPdf(http.Controller):
#     @http.route('/batch_payment_pdf/batch_payment_pdf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/batch_payment_pdf/batch_payment_pdf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('batch_payment_pdf.listing', {
#             'root': '/batch_payment_pdf/batch_payment_pdf',
#             'objects': http.request.env['batch_payment_pdf.batch_payment_pdf'].search([]),
#         })

#     @http.route('/batch_payment_pdf/batch_payment_pdf/objects/<model("batch_payment_pdf.batch_payment_pdf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('batch_payment_pdf.object', {
#             'object': obj
#         })
