import os

from odoo.tests import tagged, TransactionCase
from odoo.models.l10n_mx_cfdi.spec.lib.cfdv40 import Comprobante
from xsdata.formats.dataclass.parsers import XmlParser


@tagged('-standard', 'l10n_mx_cfdi')
class TestCFDIDocument_4_0Model(TransactionCase):
    """
    Test importing and exporting CFDI XML files into Comprobante class
    """

    def setUp(self):
        # resolve xml file path
        self.cfdi_invoice_4_0_xml_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            'cfdi_4_0_invoice.xml',
        )

        self.assertTrue(os.path.exists(self.cfdi_invoice_4_0_xml_path))

        self.cfdi_invoice_4_0_data = open(self.cfdi_invoice_4_0_xml_path, 'rb').read()

    def test_import_xml(self):
        """
        Test importing cfdi_4_0_invoice.xml into Comprobante class
        """

        parser = XmlParser()
        invoice_cfdi = parser.from_bytes(self.cfdi_invoice_4_0_data, Comprobante)
        self.assertTrue(invoice_cfdi)
