from odoo import models, api, fields


class CFDISeries(models.Model):
    _name = "l10n_mx_cfdi.series"
    _inherit = ["ir.sequence"]
    _description = "CFDI Series"

    code = fields.Char(string="Code", copy=False)

    # override create method to set the code
    @api.model
    def create(self, vals):
        if not vals.get("implementation"):
            vals["implementation"] = "no_gap"

        return super(CFDISeries, self).create(vals)
