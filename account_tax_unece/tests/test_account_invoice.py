# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestAccountInvoice(HttpCase):

    # Since odoo v9, there are no more demo invoices.
    # This method is used by both account_invoice_ubl and
    # account_invoice_factur-x. As those 2 modules use account_payment_unece,
    # it allows to factorise the code.
    # Creating a new invoice in automated tests requires so many lines of code
    # that I decided to mutualise the code here.
    def test_only_create_invoice(
        self, product=False, qty=1, price=12.42, discount=0, validate=True
    ):
        aio = self.env["account.move"]
        aao = self.env["account.account"]
        ato = self.env["account.tax"]
        company = self.env.ref("base.main_company")
        account_revenue = aao.search(
            [("code", "=", "707100"), ("company_id", "=", company.id)], limit=1
        )
        if not account_revenue:
            account_revenue = aao.create(
                {
                    "code": "707100",
                    "name": "Product Sales - (test)",
                    "company_id": company.id,
                    "user_type_id": self.env.ref(
                        "account.data_account_type_revenue"
                    ).id,
                }
            )
        taxes = ato.search(
            [
                ("company_id", "=", company.id),
                ("type_tax_use", "=", "sale"),
                ("unece_type_id", "!=", False),
                ("unece_categ_id", "!=", False),
                ("amount_type", "=", "percent"),
            ]
        )
        if taxes:
            tax = taxes[0]
        else:
            unece_type_id = self.env.ref("account_tax_unece.tax_type_vat").id
            unece_categ_id = self.env.ref("account_tax_unece.tax_categ_s").id
            tax = ato.create(
                {
                    "name": u"German VAT purchase 18.0%",
                    "description": "DE-VAT-sale-18.0",
                    "company_id": company.id,
                    "type_tax_use": "sale",
                    "price_include": False,
                    "amount": 18,
                    "amount_type": "percent",
                    "unece_type_id": unece_type_id,
                    "unece_categ_id": unece_categ_id,
                }
            )
        # validate invoice
        if not product:
            product = self.env.ref("product.product_product_4")
        invoice = aio.create(
            {
                "partner_id": self.env.ref("base.res_partner_2").id,
                "currency_id": self.env.ref("base.EUR").id,
                "type": "out_invoice",
                "company_id": company.id,
                "name": "SO1242",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "product_uom_id": product.uom_id.id,
                            "quantity": qty,
                            "price_unit": price,
                            "discount": discount,
                            "name": product.name,
                            "account_id": account_revenue.id,
                            "tax_ids": [(6, 0, [tax.id])],
                        },
                    )
                ],
            }
        )
        if validate:
            invoice.action_post()
        return invoice

    def test_get_tax_vals(self):
        tax_templates = self.env["account.tax.template"].search([])
        for template in tax_templates:
            template.unece_type_id = self.env.ref("account_tax_unece.tax_type_aaa")
            template.unece_categ_id = self.env.ref("account_tax_unece.tax_categ_a")
            template.unece_due_date_id = self.env.ref("account_tax_unece.date_5")
            res = template._get_tax_vals(self.env.company, {})
            self.assertTrue(res["unece_type_id"])
            self.assertTrue(res["unece_categ_id"])
            self.assertTrue(res["unece_due_date_id"])
            template.unece_type_id = False
            template.unece_categ_id = False
            template.unece_due_date_id = False
            res = template._get_tax_vals(self.env.company, {})
            self.assertFalse(res["unece_type_id"])
            self.assertFalse(res["unece_categ_id"])
            self.assertFalse(res["unece_due_date_id"])
