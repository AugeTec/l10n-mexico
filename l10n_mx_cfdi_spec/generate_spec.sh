#!/bin/bash

# This script is used to update the spec file with the latest changes
# in the module. It is used by the maintainer to update the spec file
# and then commit the changes.

# This script is not intended to be used by the end user.

# check if xsdata-odoo pip package is installed
INSTALLED_PIP_PACKAGES=$(pip list)
if [[ $INSTALLED_PIP_PACKAGES != *"xsdata-odoo"* ]]; then
  echo "Please install the xsdata-odoo pip package."
  echo "You can do it by running: "
  echo "pip install xsdata[cli]"
  echo "pip install git+https://github.com/akretion/xsdata-odoo"
  exit 1
fi

# make sure we are in the right directory
if [ ! -f "generate_spec.sh" ]; then
  echo "Please run this script from the module root directory."
  exit 1
fi

CFD_4_0_SCHEMA_URL="http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"
SCHEMAS_DIR="$PWD/data/schemas"

# download xsd files from the SAT if they don't exist
if [ ! -f "$SCHEMAS_DIR/4/cfdv40.xsd" ]; then
  xsdata download -o $SCHEMAS_DIR $CFD_4_0_SCHEMA_URL
fi

# remove enum values elements `<xs:enumeration value=.*/>` from $SCHEMAS_DIR/catalogos/catCFDI.xsd
# because they just make the spec file bigger and they will be stored in the database anyway

mv "$SCHEMAS_DIR/catalogos/catCFDI.xsd" "$SCHEMAS_DIR/catalogos/catCFDI.xsd.bak"
sed '/<xs:enumeration value=.*/d' "$SCHEMAS_DIR/catalogos/catCFDI.xsd.bak" >"$SCHEMAS_DIR/catalogos/catCFDI.xsd"
rm "$SCHEMAS_DIR/catalogos/catCFDI.xsd.bak"

# generate the spec file
export XSDATA_SCHEMA="l10n_mx_cfdi"
export XSDATA_VERSION="4_0"
export XSDATA_LANG=spanish
xsdata generate "$SCHEMAS_DIR/4/cfdv40.xsd" -p models.lib
xsdata generate "$SCHEMAS_DIR/4/cfdv40.xsd" -p models.mixin --output=odoo

## Add schema location and namespace map to package lib/__init__.py
cat <<EOF >>models/lib/__init__.py

CFDI_4_0_SCHEMA_LOCATION = "http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"

CFDI_4_0_NAMESPACES = {
    'cfdi': 'http://www.sat.gob.mx/cfd/4',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}
EOF
