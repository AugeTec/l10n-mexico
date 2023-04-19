from odoo import models


class CFDIMixin(models.AbstractModel):
    _name = 'spec.mixin.l10n_mx_cfdi'
    _description = 'Abstract model CFDI Mixin XSD'
    _field_prefix = "l10n_mx_"
    _schema_name = "cfdi"
    _schema_version = "4.0"
    _odoo_module = "comprobante"
    _spec_module = "odoo.addons.l10n_mx_cfdi.models.spec.mixin.cfdv40"
    _binding_module = "odoo.addons.l10n_mx_cfdi.models.spec.lib.cfdv40"
