# Copyright 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# Copyright 2017  Creu Blanca <www.creublanca.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ISO 3166",
    "version": "13.0.1.0.0",
    "author": "Tecnativa, Creu Blanca, Odoo Community Association (OCA)",
    "category": "Localization",
    "website": "https://github.com/OCA/community-data-files",
    "license": "AGPL-3",
    "depends": ["base"],
    "external_dependencies": {"python": ["pycountry"]},
    "data": ["views/country_view.xml"],
    "installable": True,
}
