from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Backfill account.payment.related_cert_ids for payment CFDIs that only
    kept the reverse link (l10n_mx_cfdi.document.related_payment_id) after
    the pre-19.0 data migration, then recompute cfdi_document_id.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    orphan_docs = env["l10n_mx_cfdi.document"].search(
        [
            ("type", "=", "P"),
            ("state", "=", "published"),
            ("related_payment_id", "!=", False),
        ]
    )
    for doc in orphan_docs:
        if doc not in doc.related_payment_id.related_cert_ids:
            doc.related_payment_id.related_cert_ids |= doc

    payments = env["account.payment"].search([("related_cert_ids", "!=", False)])
    payments._compute_cfdi_document_id()
