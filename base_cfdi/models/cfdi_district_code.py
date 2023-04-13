from odoo import api, fields, models


class CfdiDistrictCode(models.Model):
    _name = 'base_cfdi.cfdi_district_code'
    _description = 'CFDI District Code (c_Colonia)'

    name = fields.Char(
        string='Name',
        required=True,
    )

    code = fields.Char(
        string='Code',
        required=True,
    )

    zip_code = fields.Char(
        string='Zip',
        required=True,
    )
