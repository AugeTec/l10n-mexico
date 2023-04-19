from odoo import api, fields, models


class CFDIPaymentMethod(models.Model):
    _name = 'l10n_mx_cfdi.cfdi_payment_method'
    _description = 'CFDI Payment Method (c_MetodoPago)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
