# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Determine BIC from IBAN",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Infer the bank (or the bank's BIC) from the IBAN filled in",
    "depends": [
        'base_iban',
        'account',
    ],
    "data": [
        "views/res_bank_iban_bic_mapping.xml",
        "views/menu.xml",
        "data/res_bank_iban_bic_mapping_nl.xml",
        'security/ir.model.access.csv',
    ],
}
