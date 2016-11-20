# -*- coding: utf-8 -*-
from openerp import http

# class Sparkit(http.Controller):
#     @http.route('/sparkit/sparkit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sparkit/sparkit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sparkit.listing', {
#             'root': '/sparkit/sparkit',
#             'objects': http.request.env['sparkit.sparkit'].search([]),
#         })

#     @http.route('/sparkit/sparkit/objects/<model("sparkit.sparkit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sparkit.object', {
#             'object': obj
#         })