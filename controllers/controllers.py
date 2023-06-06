# -*- coding: utf-8 -*-
# from odoo import http


# class MrpProcessing(http.Controller):
#     @http.route('/mrp_processing/mrp_processing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_processing/mrp_processing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_processing.listing', {
#             'root': '/mrp_processing/mrp_processing',
#             'objects': http.request.env['mrp_processing.mrp_processing'].search([]),
#         })

#     @http.route('/mrp_processing/mrp_processing/objects/<model("mrp_processing.mrp_processing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_processing.object', {
#             'object': obj
#         })
