from odoo import api, fields, models


class CFDIReportingPeriod(models.Model):
    _name = 'base_cfdi.cfdi_reporting_period'
    _description = 'CFDI Reporting Period (c_Meses)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
