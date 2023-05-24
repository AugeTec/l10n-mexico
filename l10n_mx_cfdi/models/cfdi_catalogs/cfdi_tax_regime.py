from odoo import fields, models


class CFDITaxRegime(models.Model):
    _name = "l10n_mx_cfdi.cfdi_tax_regime"
    _description = "CFDI Tax Regime"
    _inherit = "l10n_mx_cfdi.catalog_mixin"
    _l10n_mx_catalog_name = "c_RegimenFiscal"

    applicable_to_natural_person = fields.Boolean("Applicable to Natural Person")
    applicable_to_legal_entity = fields.Boolean("Applicable to Legal Entity")