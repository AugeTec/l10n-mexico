from base64 import b64decode

from lxml import etree
from odoo.addons.l10n_mx_cfdi.libs.xsdata_class_importer import XSDataClassImporter
from odoo.addons.l10n_mx_cfdi_spec.models.lib import Comprobante

from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.parsers import XmlParser

from odoo import models, fields, _
from odoo.exceptions import UserError


class CFDIDocumentImportWizard(models.TransientModel):
    _name = "l10n_mx_cfdi.cfdi_document_import_wizard"
    _description = "CFDI Document Import Wizard"

    xml_file = fields.Binary(
        string="XML File",
        required=True,
    )

    def action_import_cfdi(self):
        try:
            # decode xml_file from base64
            xml_data = b64decode(self.xml_file)

            # parse xml_data into Comprobante class
            xml_parser = XmlParser()
            orig_dataclass = xml_parser.from_bytes(xml_data, Comprobante)

            # import Comprobante class into l10n_mx_cfdi.document_4_0 model
            document_model = self.env["l10n_mx_cfdi.document_4_0"]
            importer = XSDataClassImporter(self.env, document_model, "l10n_mx_cfdi4_0_")
            rec = importer.import_obj(orig_dataclass)
            rec.action_check_status()
        except ParserError as e:
            # notify user of error
            raise UserError(_("Error parsing XML file: %s") % e)

        return {
            "type": "ir.actions.act_window",
            "name": "CFDI Documents",
            "res_model": "l10n_mx_cfdi.document_4_0",
            "view_mode": "tree,form",
            "domain": [("id", "in", rec.ids)],
        }
