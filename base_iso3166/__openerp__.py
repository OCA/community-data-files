# -*- coding: utf-8 -*-
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ISO 3166",
    "version": "8.0.1.0.0",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "category": "Localization",
    "website": "https://odoo-community.org",
    "license": "AGPL-3",
    "depends": [
        "base"
    ],
    'external_dependencies': {
        'python': [
            'pycountry',
        ],
    },
    "data": [
        "views/country_view.xml",
    ],
    "installable": True,
}
