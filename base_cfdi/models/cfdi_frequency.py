from odoo import api, fields, models


class CFDIFrequency(models.Model):
    _name = 'base_cfdi.cfdi_frequency'
    _description = 'CFDI Frequency (c_Periodicidad)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
