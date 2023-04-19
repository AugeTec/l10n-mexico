from odoo import api, fields, models


class CFDIMunicipalityCode(models.Model):
    _name = 'l10n_mx_cfdi.cfdi_municipality_code'
    _description = 'CFDI Municipality Code (c_Municipio)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    state_id = fields.Many2one(
        'res.country.state',
        'State',
        required=True,
    )

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
