# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Numérigraphe SARL.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "European NACE partner categories",
    "version": "2.0",
    'author': u'Numérigraphe SARL, Sistheo',
    "category": "Hidden",
    "description": """This module imports the NACE rev. 2 classification
categories as partner categories in 23 languages, courtesy of the EU.

The Statistical Classification of Economic Activities in the European Community
commonly referred to as NACE, is a European industry standard classification
system consisting of a 6 digit code.
NACE is equivalent to the SIC and NAICS system:
    * Standard Industrial Classification
    * North American Industry Classification System.

This module is a rewrite of the older community module "partner_nace" from
the extra-addons repository.

The data imported into OpenERP is generated from the files downloaded
from the RAMON service:
    http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_CLS_DLD&StrNom=NACE_REV2&StrLanguageCode=DE&StrLayoutCode=#

If you want to update the data or add another translation, download the
corresponding file from RAMON using ',' as a separator, save it
to the directory "data" and name it according to the language code:
    NACE_REV2_<language code>.csv
Then update the LANGS constant in the script "make_data.py" and run it to
refresh the OpenERP data files. Finally, upgrade the module to load the data.
""",
    "data": [
        "data/res.partner.category.csv",
    ],
}
