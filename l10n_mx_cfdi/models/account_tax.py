from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    l10n_mx_cfdi_code = fields.Char('CFDI Code', help='Tax code for CFDI')
    l10n_mx_cfdi_is_retention = fields.Boolean(
        'Is Retention?',
        help='Check if this tax is a retention'
    )
    l10n_mx_cfdi_is_transferred = fields.Boolean(
        'Is Transferred?',
        help='Check if this tax is a transfer'
    )
