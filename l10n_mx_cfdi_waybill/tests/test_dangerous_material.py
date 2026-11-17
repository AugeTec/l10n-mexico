from odoo.exceptions import UserError

from ..services import waybill_builder
from .common import WaybillTestCommon


class TestWaybillDangerousMaterial(WaybillTestCommon):
    """Carta Porte 3.1 hazardous material and environmental insurance."""

    def _goods(self, waybill):
        goods, _locations = waybill._format_goods_and_locations_data()
        return goods[0]

    def _set_product(self, **vals):
        self.stock_product.product_tmpl_id.write(vals)

    def test_not_hazardous_omits_attribute(self):
        waybill = self._create_waybill()
        self._create_waybill_entry(waybill)
        self.assertNotIn("MaterialPeligroso", self._goods(waybill))

    def test_optional_flagged_to_send_reports_no(self):
        self._set_product(
            l10n_mx_cfdi_dangerous_material_optional=True,
            l10n_mx_cfdi_dangerous_material_send=True,
        )
        waybill = self._create_waybill()
        self._create_waybill_entry(waybill)
        goods = self._goods(waybill)
        self.assertEqual(goods["MaterialPeligroso"], "No")
        self.assertNotIn("CveMaterialPeligroso", goods)

    def test_hazardous_requires_code_and_packaging(self):
        self._set_product(l10n_mx_cfdi_dangerous_material_indicator=True)
        waybill = self._create_waybill()
        self._create_waybill_entry(waybill)
        with self.assertRaises(UserError):
            self._goods(waybill)

    def _make_hazardous(self):
        self._set_product(
            l10n_mx_cfdi_dangerous_material_indicator=True,
            l10n_mx_cfid_dangerous_material_code="1203",
            l10n_mx_cfid_dangerous_material_packaging="4H2",
            l10n_mx_cfid_dangerous_material_packaging_descripcion="Cajas de plástico",
        )

    def test_hazardous_goods_node_and_builder(self):
        self._make_hazardous()
        waybill = self._create_waybill()
        self._create_waybill_entry(waybill)
        goods = self._goods(waybill)
        self.assertEqual(goods["MaterialPeligroso"], "Sí")
        self.assertEqual(goods["CveMaterialPeligroso"], "1203")
        self.assertEqual(goods["Embalaje"], "4H2")
        mercancia = waybill_builder._build_mercancia([goods])[0]
        self.assertEqual(mercancia["MaterialPeligroso"], "Sí")
        self.assertEqual(mercancia["CveMaterialPeligroso"], "1203")
        self.assertEqual(mercancia["DescripEmbalaje"], "Cajas de plástico")

    def test_hazardous_requires_environmental_insurance(self):
        self._make_hazardous()
        waybill = self._create_waybill()
        self._create_waybill_entry(waybill)
        with self.assertRaises(UserError):
            waybill._format_data()

    def test_environmental_insurance_in_seguros(self):
        self._make_hazardous()
        self.vehicle.write(
            {
                "environmental_insurance_company": "Aseguradora Verde",
                "environmental_insurance_number": "MA-123",
            }
        )
        waybill = self._create_waybill()
        self._create_waybill_entry(waybill)
        data = waybill._format_data()
        auto = data["Complemento"]["CartaPorte31"]["Mercancias"]["Autotransporte"]
        self.assertEqual(auto["Seguros"]["AseguraMedAmbiente"], "Aseguradora Verde")
        self.assertEqual(auto["Seguros"]["PolizaMedAmbiente"], "MA-123")
        built = waybill_builder._build_autotransporte(auto)
        self.assertEqual(built["Seguros"]["PolizaMedAmbiente"], "MA-123")
