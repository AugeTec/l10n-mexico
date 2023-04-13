from odoo import api, fields, models


class CFDITaxRegime(models.Model):
    _name = 'base_cfdi.cfdi_tax_regime'
    _description = 'CFDI Tax Regime (c_RegimenFiscal)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    applicable_to_natural_person = fields.Boolean('Applicable to Natural Person')
    applicable_to_legal_entity = fields.Boolean('Applicable to Legal Entity')

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
