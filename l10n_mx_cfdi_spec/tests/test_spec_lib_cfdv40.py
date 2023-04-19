import decimal
import os

from odoo.tests import tagged, TransactionCase
from odoo.addons.l10n_mx_cfdi_spec.models.lib import Comprobante
from xsdata.formats.dataclass.parsers import XmlParser

from odoo.tools import float_compare


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

        ###
        # Check that CFDI fields are correctly loaded from xml_data
        ###

        # check CFDI general fields
        self.assertEqual(invoice_cfdi.version, "4.0")
        self.assertEqual(invoice_cfdi.serie, "I")
        self.assertEqual(invoice_cfdi.folio, "22")
        self.assertEqual(invoice_cfdi.fecha, "2023-04-11T20:17:00")
        self.assertTrue(invoice_cfdi.sello)
        self.assertEqual(invoice_cfdi.forma_pago, "99")
        self.assertEqual(invoice_cfdi.no_certificado, "30001000000400002434")
        self.assertTrue(invoice_cfdi.certificado)
        self.assertEqual(invoice_cfdi.sub_total, "200.00")
        self.assertEqual(invoice_cfdi.moneda, "MXN")
        self.assertEqual(invoice_cfdi.total, "232.00")
        self.assertEqual(invoice_cfdi.tipo_de_comprobante, "I")
        self.assertEqual(invoice_cfdi.metodo_pago, "PPD")
        self.assertEqual(invoice_cfdi.exportacion, "01")
        self.assertEqual(invoice_cfdi.lugar_expedicion, "26015")

        # check CFDI Emisor fields
        emisor = invoice_cfdi.emisor
        self.assertEqual(emisor.rfc, "EKU9003173C9")
        self.assertEqual(emisor.nombre, "ESCUELA KEMPER URGATE")
        self.assertEqual(emisor.regimen_fiscal, "601")

        # check CFDI Receptor fields
        receptor = invoice_cfdi.receptor
        self.assertEqual(receptor.rfc, "CACX7605101P8")
        self.assertEqual(receptor.nombre, "XOCHILT CASAS CHAVEZ")
        self.assertEqual(receptor.domicilio_fiscal_receptor, "10740")
        self.assertEqual(receptor.regimen_fiscal_receptor, "612")
        self.assertEqual(receptor.uso_cfdi, "G03")

        # check CFDI Conceptos fields
        conceptos = invoice_cfdi.conceptos.concepto
        self.assertEqual(len(conceptos), 1)
        concepto = conceptos[0]
        self.assertEqual(concepto.clave_prod_serv, "01010101")
        self.assertEqual(concepto.no_identificacion, "false")
        self.assertEqual(concepto.cantidad, 1.0)
        self.assertEqual(concepto.clave_unidad, "H87")
        self.assertEqual(concepto.descripcion, "Producto 1")
        self.assertEqual(concepto.valor_unitario, "200.00")
        self.assertEqual(concepto.importe, "200.00")
        self.assertEqual(concepto.objeto_imp, "02")

        impuestos_traslados = concepto.impuestos.traslados.traslado
        self.assertEqual(len(impuestos_traslados), 1)
        impuesto_traslado = impuestos_traslados[0]
        self.assertEqual(impuesto_traslado.base, 200.00)
        self.assertEqual(impuesto_traslado.impuesto, "002")
        self.assertEqual(impuesto_traslado.tipo_factor, "Tasa")
        self.assertEqual(
            impuesto_traslado.tasa_ocuota,
            decimal.Decimal("0.160000")
        )
        self.assertEqual(impuesto_traslado.importe, "32.00")
