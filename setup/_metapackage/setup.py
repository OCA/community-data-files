import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-community-data-files",
    description="Meta package for oca-community-data-files Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-account_payment_unece',
        'odoo11-addon-account_tax_unece',
        'odoo11-addon-base_bank_from_iban',
        'odoo11-addon-base_iso3166',
        'odoo11-addon-base_unece',
        'odoo11-addon-product_uom_unece',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
