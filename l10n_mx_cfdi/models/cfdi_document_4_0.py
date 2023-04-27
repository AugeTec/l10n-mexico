from odoo.addons.spec_driven_model.models import spec_models

from odoo import fields


class CFDI_4_0(spec_models.SpecModel):
    """
    Base Model for CFDI 4.0 Documents

    This model is used to hold the CFDI 4.0 documents and to be able to
    import/export them. It inherits from `l10n_mx_cfdi.4_0.comprobante`
    mixin by means of the spec_driven_model module. The mixin is generated
    from the CFDI 4.0 XSD schema using xsdata-odoo.

    This performs the following tasks:
    - Link the catalog fields to the corresponding catalog models
    - Validate the CFDI document against the specification
    - Generate the XML file from the CFDI document
    - Generate the CFDI document from the XML file
    """

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
