from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    l10n_mx_cfdi_dangerous_material_indicator = fields.Boolean(string="Indicador de material peligroso CFDI",
                                                               default=False)
    l10n_mx_cfdi_dangerous_material_optional = fields.Boolean(string="Material peligroso opcional CFDI",
                                                              default=False)
    l10n_mx_cfid_dangerous_material_code = fields.Char(string="Código de Material Peligroso")

    l10n_mx_cfid_dangerous_material_packaging = fields.Char(string="Código de Embalaje Material Peligroso")

    l10n_mx_cfid_dangerous_material_packaging_descripcion = fields.Char(string="Descripción de Embalaje Material Peligroso")

    l10n_mx_cfdi_dangerous_material_send = fields.Boolean(string="Enviar Clave Material Peligroso",
                                                              default=False,
                                                                help = (
                                                                    "Controla si el atributo MaterialPeligroso se envía a Facturama. "
                                                                    "Consulte la columna 'Material peligroso' de la clave BienesTransp "
                                                                    "en el catálogo SAT c_ClaveProdServCP. "
                                                                    "No marque este campo cuando el catálogo indique '0', porque el "
                                                                    "atributo debe omitirse completamente y Facturama rechazará el CFDI "
                                                                    "aunque se envíe con el valor 'No'. "
                                                                    "Márquelo cuando el catálogo indique '1' o '0,1'. "
                                                                    "Para '1', la mercancía debe enviarse como 'Sí'. "
                                                                    "Para '0,1', seleccione 'Sí' o 'No' según la mercancía transportada."
                                                                ),
                                                          )
