from odoo import api, fields, models


class CfdiMeasurementUnit(models.Model):
    _name = 'base_cfdi.cfdi_measurement_unit'
    _description = 'CFDI Measurement Unit (c_ClaveUnidad)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)  # column 'Nombre'
    detail = fields.Char('Detail')  # column 'Descripción'
    notes = fields.Char('Notes')  # column 'Notas'
    symbol = fields.Char('Symbol')  # column 'Símbolo'

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
