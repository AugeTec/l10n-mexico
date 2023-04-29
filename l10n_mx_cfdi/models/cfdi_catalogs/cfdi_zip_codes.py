from odoo import api, fields, models


class CFDIZipCodes(models.Model):
    _name = "l10n_mx_cfdi.cfdi_zip_codes"
    _description = "CFDI Zip Codes (c_CodigoPostal)"
    _inherit = "l10n_mx_cfdi.catalog_mixin"

    state_id = fields.Many2one("res.country.state", "State", required=True)
    municipality_id = fields.Many2one(
        "l10n_mx_cfdi.cfdi_municipality_code", "Municipality"
    )
    locality_id = fields.Many2one("l10n_mx_cfdi.cfdi_locality_code", "Locality")
