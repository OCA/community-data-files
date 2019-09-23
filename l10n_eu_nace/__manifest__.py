# Copyright 2011 Numérigraphe SARL.
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "European NACE partner categories",
    "version": "12.0.2.0.0",
    'author': u'Numérigraphe SARL,'
              u'Sistheo,Odoo Community Association (OCA)',
    "category": "Localization",
    "data": [
        'views/res_partner.xml',
        'security/res_partner_nace.xml',
        'views/res_partner_nace.xml',
        "data/res.partner.nace.csv",
    ],
    'depends': ['contacts'],
    'installable': True,
    'license': 'AGPL-3',
}
