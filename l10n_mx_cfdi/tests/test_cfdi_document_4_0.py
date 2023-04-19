import os

from xsdata.formats.dataclass.parsers import XmlParser

from odoo.tests import SavepointCase, tagged


@tagged('-standard', 'l10n_mx_cfdi')
class TestCFDIDocument_4_0Model(SavepointCase):
    """
    Test importing and exporting CFDI XML files into CFDIDocument_4_0 model
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
        Test importing cfdi_4_0_invoice.xml into CFDIDocument_4_0 model
        """

        document_model = self.env['l10n_mx_cfdi.document_4_0']
        self.assertTrue(document_model)
