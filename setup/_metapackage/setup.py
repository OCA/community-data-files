import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-community-data-files",
    description="Meta package for oca-community-data-files Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-account_payment_unece',
        'odoo8-addon-account_tax_unece',
        'odoo8-addon-base_iso3166',
        'odoo8-addon-base_unece',
        'odoo8-addon-l10n_eu_nace',
        'odoo8-addon-product_uom_unece',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
