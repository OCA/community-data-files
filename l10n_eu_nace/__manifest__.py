# Copyright 2011 Numérigraphe SARL.
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "European NACE partner categories",
    "version": "14.0.1.0.0",
    "author": "Numérigraphe SARL, Sistheo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "category": "Localization",
    "data": [
        "data/res.partner.nace.csv",
        "security/res_partner_nace.xml",
        "views/res_partner.xml",
        "views/res_partner_nace.xml",
    ],
    "depends": ["contacts"],
    "installable": True,
    "license": "AGPL-3",
}
