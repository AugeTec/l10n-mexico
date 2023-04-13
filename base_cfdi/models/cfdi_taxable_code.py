from odoo import api, fields, models


class CfdiTaxableCode(models.Model):
    _name = 'base_cfdi.cfdi_taxable_code'
    _description = 'CFDI Taxable Code (c_ObjetoImp)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)  # column 'Nombre'

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
