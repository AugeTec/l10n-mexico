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

# download xsd files from the SAT if they don't exist
if [ ! -f "/tmp/cfd_schemas/4/cfdv40.xsd" ]; then
  xsdata download -o /tmp/cfd_schemas $CFD_4_0_SCHEMA_URL
fi

# remove enum values elements `<xs:enumeration value=.*/>` from /tmp/cfd_schemas/catalogos/catCFDI.xsd
# because they cause problems with xsdata

mv /tmp/cfd_schemas/catalogos/catCFDI.xsd /tmp/cfd_schemas/catalogos/catCFDI.xsd.bak
sed '/<xs:enumeration value=.*/d' /tmp/cfd_schemas/catalogos/catCFDI.xsd.bak >/tmp/cfd_schemas/catalogos/catCFDI.xsd

# generate the spec file
export XSDATA_SCHEMA="l10n_mx_cfdi"
export XSDATA_VERSION="4_0"
export XSDATA_LANG=spanish
xsdata generate /tmp/cfd_schemas/4/cfdv40.xsd -p models.spec.lib
xsdata generate /tmp/cfd_schemas/4/cfdv40.xsd -p models.spec.mixin --output=odoo
