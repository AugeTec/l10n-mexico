from odoo import models


class CFDISpecModel(models.AbstractModel):
    _description = "Abstract model CFDI Mixin XSD"
    _name = "spec.mixin.l10n_mx_cfdi"
    _field_prefix = "l10n_mx_cfdi4_0_"
    _schema_name = "cfdi"
    _schema_version = "4.0"
    _odoo_module = "odoo.addons.l10n_mx_cfdi"
    _spec_module = "odoo.addons.l10n_mx_cfdi_spec.models.mixin.comprobante"
    _binding_module = "odoo.addons.l10n_mx_cfdi_spec.models.lib.comprobante"
    _spec_tab_name = "CFDI"
    _inherit = "spec.mixin"

    def _valid_field_parameter(self, field, name):
        if name in ("xsd_type", "xsd_required", "choice", "xsd_implicit"):
            return True
        else:
            return super()._valid_field_parameter(field, name)
