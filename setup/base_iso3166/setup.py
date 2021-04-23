import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'external_dependencies_override': {
            'python': {
                'pycountry': 'pycountry<18.12.8',
            },
        },
    },
)
