import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-community-data-files",
    description="Meta package for oca-community-data-files Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-base_bank_from_iban',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
