from odoo.tools.sql import column_exists, create_column


def migrate(cr, version):
    """Keep existing services on Facturama when introducing multi-PAC.

    Before 19.0.2.1.0 Facturama was the only supported PAC, so services
    created then must not fall back to the new ``provider`` default.
    """
    if not version or column_exists(cr, "l10n_mx_cfdi_cfdi_service", "provider"):
        return
    create_column(cr, "l10n_mx_cfdi_cfdi_service", "provider", "varchar")
    cr.execute("UPDATE l10n_mx_cfdi_cfdi_service SET provider = 'facturama'")
