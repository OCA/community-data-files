# Copyright 2019 Camptocamp SA
# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "ADR Dangerous Goods",
    "summary": "Allows to set appropriate danger class and components",
    "version": "18.0.1.0.0",
    "category": "Inventory/Delivery",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Opener B.V., Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock"],
    "development_status": "Beta",
    "data": [
        "data/uom_uom.xml",
        "data/adr_class.xml",
        "data/adr_label.xml",
        "data/adr_packing_instruction.xml",
        "data/adr_goods.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/adr_class_views.xml",
        "views/adr_goods_views.xml",
        "views/adr_label_views.xml",
        "views/adr_packing_instruction_views.xml",
        "views/menu.xml",
        # NB. product template views need to come before product product views
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/stock_picking_views.xml",
    ],
}
