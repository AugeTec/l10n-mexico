from odoo import api, fields, models


class CFDIProductAndServiceCode(models.Model):
    _name = 'base_cfdi.cfdi_product_and_service_code'
    _description = 'CFDI Product and Service Code (c_ClaveProdServ)'

    name = fields.Char('Name', compute='_compute_name', store=True)
    code = fields.Char('Code', required=True)
    description = fields.Char('Description', required=True)

    include_transferred_iva = fields.Selection([
        ('0', 'No'),
        ('1', 'Yes'),
        ('2', 'Optional'),
    ], string='Include Transferred IVA', required=True, default='2')

    include_transferred_ieps = fields.Selection([
        ('0', 'No'),
        ('1', 'Yes'),
        ('2', 'Optional'),
    ], string='Include Transferred IEPS', required=True, default='2')

    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = record.code + ' - ' + record.description
