import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-community-data-files",
    description="Meta package for oca-community-data-files Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-account_payment_unece',
        'odoo12-addon-account_tax_unece',
        'odoo12-addon-base_bank_from_iban',
        'odoo12-addon-base_currency_iso_4217',
        'odoo12-addon-base_iso3166',
        'odoo12-addon-base_unece',
        'odoo12-addon-l10n_eu_nace',
        'odoo12-addon-product_fao_fishing',
        'odoo12-addon-uom_unece',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
