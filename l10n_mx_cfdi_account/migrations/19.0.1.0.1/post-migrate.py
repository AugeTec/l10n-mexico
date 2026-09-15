from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    payments = env["account.payment"].search([("related_cert_ids", "!=", False)])
    payments._compute_cfdi_document_id()
