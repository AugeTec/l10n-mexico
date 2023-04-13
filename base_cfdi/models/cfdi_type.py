from odoo import api, fields, models


class CFDIType(models.Model):
    _name = 'base_cfdi.cfdi_type'
    _description = 'CFDI Type (c_TipoDeComprobante)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
