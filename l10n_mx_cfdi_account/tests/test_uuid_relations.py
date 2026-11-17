from satcfdi.create.cfd import cfdi40

from .common import CFDIAccountTestCommon

UUID_A = "11111111-1111-1111-1111-111111111111"
UUID_B = "22222222-2222-2222-2222-222222222222"
UUID_C = "33333333-3333-3333-3333-333333333333"


class TestAccountMoveUuidRelations(CFDIAccountTestCommon):
    """Free-text UUID relations (account.move.document.relation)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.type_01 = cls.env.ref("l10n_mx_catalogs.c_tipo_relacion_1")
        cls.type_04 = cls.env.ref("l10n_mx_catalogs.c_tipo_relacion_4")

    def _invoice_with_uuid_relations(self, *relations):
        invoice = self._create_cfdi_invoice()
        invoice.cfdi_document_relation_ids = [
            (0, 0, {"relation_type_id": rel_type.id, "target_uuid": uuid})
            for rel_type, uuid in relations
        ]
        return invoice

    def test_no_relations_returns_none(self):
        invoice = self._create_cfdi_invoice()
        self.assertIsNone(invoice._with_uuid_relations(None))

    def test_uuid_relations_only(self):
        invoice = self._invoice_with_uuid_relations((self.type_04, UUID_A))
        node = invoice._with_uuid_relations(None)
        self.assertEqual(node["TipoRelacion"], self.type_04.code)
        self.assertEqual(node["CfdiRelacionado"], [UUID_A])

    def test_same_type_merges_into_existing_node(self):
        invoice = self._invoice_with_uuid_relations(
            (self.type_01, UUID_B), (self.type_01, UUID_A)
        )
        base = cfdi40.CfdiRelacionados(
            tipo_relacion=self.type_01.code, cfdi_relacionado=[UUID_A]
        )
        node = invoice._with_uuid_relations(base)
        # one node per type, duplicated UUID not repeated
        self.assertEqual(node["TipoRelacion"], self.type_01.code)
        self.assertEqual(node["CfdiRelacionado"], [UUID_A, UUID_B])

    def test_different_types_give_one_node_each(self):
        invoice = self._invoice_with_uuid_relations((self.type_04, UUID_C))
        base = cfdi40.CfdiRelacionados(
            tipo_relacion=self.type_01.code, cfdi_relacionado=[UUID_A]
        )
        nodes = invoice._with_uuid_relations(base)
        self.assertEqual(len(nodes), 2)
        by_type = {n["TipoRelacion"]: n["CfdiRelacionado"] for n in nodes}
        self.assertEqual(by_type[self.type_01.code], [UUID_A])
        self.assertEqual(by_type[self.type_04.code], [UUID_C])

    def test_invoice_comprobante_includes_uuid_relations(self):
        invoice = self._post_cfdi_invoice(
            self._invoice_with_uuid_relations((self.type_04, UUID_C))
        )
        comprobante = invoice._gather_invoice_cfdi_data()
        related = comprobante["CfdiRelacionados"]
        related = related if isinstance(related, list) else [related]
        self.assertEqual(related[0]["TipoRelacion"], self.type_04.code)
        self.assertEqual(related[0]["CfdiRelacionado"], [UUID_C])
