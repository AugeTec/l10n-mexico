from odoo import api, fields, models


class CFDIUse(models.Model):
    _name = 'base_cfdi.cfdi_use'
    _description = 'CFDI Use (c_UsoCFDI)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)
    similar_terms = fields.Char('Similar Terms')

    applicable_to_natural_person = fields.Boolean(
        'Applicable to Natural Person'
    )
    applicable_to_legal_entity = fields.Boolean('Applicable to Legal Entity')

    tax_regime_ids = fields.Many2many('base_cfdi.cfdi_tax_regime',
                                      'base_cfdi_cfdi_use_tax_regime_rel',
                                      'Applicable to Tax Regimes')

    border_zone_incentive = fields.Integer('Border Zone Incentive')

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
