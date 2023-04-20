from .comprobante import Comprobante

__all__ = [
    "Comprobante",
]

CFDI_4_0_SCHEMA_LOCATION = "http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"

CFDI_4_0_NAMESPACES = {
    'cfdi': 'http://www.sat.gob.mx/cfd/4',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}
