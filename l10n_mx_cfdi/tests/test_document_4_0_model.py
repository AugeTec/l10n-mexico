import os

from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer

from odoo.tests import tagged, TransactionCase

from odoo.addons.l10n_mx_cfdi.libs.xsdata_class_exporter import XSDataClassExporter
from odoo.addons.l10n_mx_cfdi.libs.xsdata_class_importer import XSDataClassImporter
from odoo.addons import l10n_mx_cfdi_spec as l10n_mx_cfdi_spec_module
from odoo.addons.l10n_mx_cfdi_spec.models.lib import (
    Comprobante,
    CFDI_4_0_SCHEMA_LOCATION,
    CFDI_4_0_NAMESPACES,
)
from odoo.addons.l10n_mx_cfdi_spec.tests.utils import assert_equal_xml


@tagged("-standard", "l10n_mx_cfdi")
class TestCFDIDocument_4_0Model(TransactionCase):
    """
    Test importing and exporting CFDI XML files into Comprobante Model
    """

    def setUp(self):
        # get Comprobante class file path

        l10n_mx_cfdi_spec_path = os.path.dirname(l10n_mx_cfdi_spec_module.__file__)
        data_dir_path = os.path.join(l10n_mx_cfdi_spec_path, "data")

        self.cfdi_invoice_4_0_xml_path = os.path.join(
            data_dir_path, "cfdi_4_0_invoice.xml"
        )
        self.cfdi_schema_path = os.path.join(data_dir_path, "schemas/4/cfdv40.xsd")
        self.assertTrue(os.path.exists(self.cfdi_invoice_4_0_xml_path))

        self.cfdi_invoice_4_0_data = open(self.cfdi_invoice_4_0_xml_path, "rb").read()

    def test_import_export_xml(self):
        """
        Test importing cfdi_4_0_invoice.xml into Comprobante class
        """

        xml_parser = XmlParser()

        orig_dataclass = xml_parser.from_bytes(self.cfdi_invoice_4_0_data, Comprobante)

        document_model = self.env["l10n_mx_cfdi.document_4_0"]
        importer = XSDataClassImporter(self.env, document_model, "l10n_mx_cfdi4_0_")
        orig_record = importer.import_obj(orig_dataclass)

        exporter = XSDataClassExporter(self.env, Comprobante, "l10n_mx_cfdi4_0_")
        exported_dataclass = exporter.export_obj(orig_record)

        # create xml from Comprobante class using  XmlSerializer
        serializer_config = SerializerConfig(
            schema_location=CFDI_4_0_SCHEMA_LOCATION,
        )
        serializer = XmlSerializer(config=serializer_config)
        xml_data = serializer.render(exported_dataclass, ns_map=CFDI_4_0_NAMESPACES)

        assert_equal_xml(self, xml_data.encode("utf-8"), self.cfdi_invoice_4_0_data)
