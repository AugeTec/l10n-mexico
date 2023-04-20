# -*- coding: utf-8 -*-
# from odoo import http


# class L10nMxCfdiSpec(http.Controller):
#     @http.route('/l10n_mx_cfdi_spec/l10n_mx_cfdi_spec', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_mx_cfdi_spec/l10n_mx_cfdi_spec/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_mx_cfdi_spec.listing', {
#             'root': '/l10n_mx_cfdi_spec/l10n_mx_cfdi_spec',
#             'objects': http.request.env['l10n_mx_cfdi_spec.l10n_mx_cfdi_spec'].search([]),
#         })

#     @http.route('/l10n_mx_cfdi_spec/l10n_mx_cfdi_spec/objects/<model("l10n_mx_cfdi_spec.l10n_mx_cfdi_spec"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_mx_cfdi_spec.object', {
#             'object': obj
#         })
