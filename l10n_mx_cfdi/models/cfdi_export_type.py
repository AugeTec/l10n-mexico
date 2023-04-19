from odoo import api, fields, models


class CFDIExportType(models.Model):
    _name = 'l10n_mx_cfdi.cfdi_export_type'
    _description = 'CFDI Export Type (c_Exportacion)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
