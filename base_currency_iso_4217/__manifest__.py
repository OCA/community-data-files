# Copyright 2018 ForgeFlow, S.L. (https://www.forgeflow.com)
# @author: Jordi Ballester <jordi.ballester@forgeflow.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Base Currency ISO 4217",
    "version": "13.0.1.0.0",
    "category": "Base",
    "license": "AGPL-3",
    "summary": "Adds numeric code and full name to currencies, "
    "following the ISO 4217 specification",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["base"],
    "data": ["data/res_currency_data.xml", "views/res_currency_views.xml"],
    "installable": True,
}
