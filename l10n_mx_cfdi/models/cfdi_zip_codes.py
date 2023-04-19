from odoo import api, fields, models


class CFDIZipCodes(models.Model):
    _name = 'l10n_mx_cfdi.cfdi_zip_codes'
    _description = 'CFDI Zip Codes (c_CodigoPostal)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    state_id = fields.Many2one('res.country.state', 'State', required=True)
    municipality_id = fields.Many2one('l10n_mx_cfdi.cfdi_municipality_code',
                                      'Municipality')
    locality_id = fields.Many2one('l10n_mx_cfdi.cfdi_locality_code', 'Locality')

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
