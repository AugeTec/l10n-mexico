from collections import defaultdict

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Backfill account.payment.related_cert_ids for payment ("P") CFDIs and
    recompute cfdi_document_id.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    cr.execute(
        """
        SELECT doc_id, array_agg(DISTINCT payment_id)
        FROM (
            SELECT d.id AS doc_id, d.related_payment_id AS payment_id
            FROM l10n_mx_cfdi_document d
            WHERE d.type = 'P' AND d.related_payment_id IS NOT NULL
            UNION
            SELECT d.id, ap.id
            FROM l10n_mx_cfdi_document d
            JOIN account_move_l10n_mx_cfdi_document_rel r
                ON r.l10n_mx_cfdi_document_id = d.id
            JOIN account_payment ap ON ap.move_id = r.account_move_id
            WHERE d.type = 'P'
        ) links
        GROUP BY doc_id
        """
    )
    docs_by_payment = defaultdict(list)
    for doc_id, payment_ids in cr.fetchall():
        if len(payment_ids) == 1:
            docs_by_payment[payment_ids[0]].append(doc_id)

    for payment in env["account.payment"].browse(docs_by_payment.keys()):
        payment.related_cert_ids = [(4, doc_id) for doc_id in docs_by_payment[payment.id]]

    payments = env["account.payment"].search([("related_cert_ids", "!=", False)])
    payments._compute_cfdi_document_id()
