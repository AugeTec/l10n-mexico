from odoo import models, fields, api, _
from odoo.addons.spec_driven_model.models import spec_models


class CFDI_4_0(spec_models.SpecModel):
    _name = 'l10n_mx_cfdi.document_4_0'
    _description = 'CFDI Document 4.0'
    _inherit = 'l10n_mx_cfdi.4_0.comprobante'

    name = fields.Char(
        string='Name',
        readonly=True,
        compute='_compute_name',
    )

    def _compute_name(self):
        for rec in self:
            prefix = f"{rec.l10n_mx_cfdi4_0_Serie}-" if rec.l10n_mx_cfdi4_0_Serie else ''
            rec.name = prefix + rec.l10n_mx_cfdi4_0_Folio