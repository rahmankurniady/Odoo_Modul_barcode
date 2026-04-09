# -*- coding: utf-8 -*-
# from odoo import http


# class IntxBarcode(http.Controller):
#     @http.route('/intx_barcode/intx_barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intx_barcode/intx_barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('intx_barcode.listing', {
#             'root': '/intx_barcode/intx_barcode',
#             'objects': http.request.env['intx_barcode.intx_barcode'].search([]),
#         })

#     @http.route('/intx_barcode/intx_barcode/objects/<model("intx_barcode.intx_barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intx_barcode.object', {
#             'object': obj
#         })

