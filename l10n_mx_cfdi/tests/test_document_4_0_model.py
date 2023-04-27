import os

from lxml import etree
from odoo.addons.l10n_mx_cfdi.libs.xsdata_class_importer import XSDataClassImporter
from odoo.addons.l10n_mx_cfdi_spec.models.lib import Comprobante
from xsdata.formats.dataclass.parsers import XmlParser

from odoo.tests import tagged, TransactionCase


@tagged('-standard', 'l10n_mx_cfdi')
class TestCFDIDocument_4_0Model(TransactionCase):
    """
    Test importing and exporting CFDI XML files into Comprobante Model
    """

    def setUp(self):
        # get Comprobante class file path
        from odoo.addons import l10n_mx_cfdi_spec
        l10n_mx_cfdi_spec_path = os.path.dirname(l10n_mx_cfdi_spec.__file__)
        data_dir_path = os.path.join(l10n_mx_cfdi_spec_path, 'data')

        self.cfdi_invoice_4_0_xml_path = os.path.join(data_dir_path, 'cfdi_4_0_invoice.xml')
        self.cfdi_schema_path = os.path.join(data_dir_path, 'schemas/4/cfdv40.xsd')
        self.assertTrue(os.path.exists(self.cfdi_invoice_4_0_xml_path))

        self.cfdi_invoice_4_0_data = open(self.cfdi_invoice_4_0_xml_path, 'rb').read()

    def test_import_export_xml(self):
        """
        Test importing cfdi_4_0_invoice.xml into Comprobante class
        """

        xml_parser = XmlParser()

        invoice = xml_parser.from_bytes(self.cfdi_invoice_4_0_data, Comprobante)

        document_model = self.env['l10n_mx_cfdi.document_4_0']
        importer = XSDataClassImporter(self.env, document_model, 'l10n_mx_cfdi4_0_')
        document = importer.import_obj(invoice)

    @staticmethod
    def assert_equal_xml_trees(xml1_data: bytes, xml2_data: bytes):
        """
        Assert that two xml trees are equal by comparing their nodes
        and attributes
        """
        xml1 = etree.fromstring(xml1_data)
        xml2 = etree.fromstring(xml2_data)

        def compare_nodes(node1, node2):
            """
            Compare two nodes by tag name, attributes and children nodes
            """
            if node1.tag != node2.tag:
                raise AssertionError(
                    f"Node tags {node1.tag} and {node2.tag} are not equal"
                )

            if node1.attrib != node2.attrib:
                raise AssertionError(
                    f"Node attributes {node1.attrib} and {node2.attrib} "
                    f"are not equal"
                )

            node_1_test = node1.text or ""
            node_2_test = node2.text or ""
            if node_1_test.strip() != node_2_test.strip():
                raise AssertionError(
                    f"Node text {node1.text} and {node2.text} are not equal"
                )

            if len(node1) != len(node2):
                raise AssertionError(
                    f"Node {etree.tostring(node1)} has {len(node1)} children "
                    f"and node {etree.tostring(node2)} has {len(node2)} children"
                )

            for child1, child2 in zip(node1, node2):
                compare_nodes(child1, child2)

        compare_nodes(xml1, xml2)
