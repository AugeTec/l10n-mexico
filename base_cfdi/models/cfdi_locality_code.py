from odoo import api, fields, models


class CFDILocalityCode(models.Model):
    _name = 'base_cfdi.cfdi_locality_code'
    _description = 'CFDI Locality Code (c_Localidad)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    state_id = fields.Many2one(
        'res.country.state',
        'State',
        required=True,
    )

    border_zone_incentive = fields.Integer(
        'Border Zone Incentive',
        help='Border Zone Incentive',
    )

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
