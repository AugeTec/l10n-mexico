from odoo import models, fields, api, _


class CFDI4(models.Model):
    _name = 'cfdi.4'
    _description = 'CFDI 4'
    _order = 'name'
    _inherit = ['cfdi.4_0.comprobante']
