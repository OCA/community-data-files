import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-community-data-files",
    description="Meta package for oca-community-data-files Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-base_unece',
        'odoo14-addon-uom_unece',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
