from odoo import fields, models, api, _


class CFDI_4_0(models.Model):
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

    _name = "l10n_mx_cfdi.document_4_0"
    _description = "CFDI Document 4.0"
    _inherit = "l10n_mx_cfdi_spec.4_0.comprobante"

    name = fields.Char(
        string="Name",
        readonly=True,
        compute="_compute_name",
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("to_post", "To Post"),
            ("posted", "Posted"),
            ("to_cancel", "To Cancel"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        readonly=True,
        copy=False,
        tracking=True,
        default="draft",
    )

    @api.depends("l10n_mx_cfdi4_0_serie", "l10n_mx_cfdi4_0_folio")
    def _compute_name(self):
        for rec in self:
            prefix = (
                f"{rec.l10n_mx_cfdi4_0_serie}-" if rec.l10n_mx_cfdi4_0_serie else ""
            )
            if rec.l10n_mx_cfdi4_0_folio:
                rec.name = prefix + rec.l10n_mx_cfdi4_0_folio
            else:
                rec.name = _("Draft")

    def action_post(self):
        pass

    def action_cancel(self):
        pass

    def action_draft(self):
        pass
