import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-community-data-files",
    description="Meta package for oca-community-data-files Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-account_payment_unece',
        'odoo13-addon-account_tax_unece',
        'odoo13-addon-base_bank_from_iban',
        'odoo13-addon-base_currency_iso_4217',
        'odoo13-addon-base_iso3166',
        'odoo13-addon-base_unece',
        'odoo13-addon-l10n_eu_adr_report',
        'odoo13-addon-l10n_eu_product_adr',
        'odoo13-addon-product_fao_fishing',
        'odoo13-addon-product_meat_unece',
        'odoo13-addon-uom_unece',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
