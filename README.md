
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/community-data-files&target_branch=13.0)
[![Pre-commit Status](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml/badge.svg?branch=13.0)](https://github.com/OCA/community-data-files/actions/workflows/pre-commit.yml?query=branch%3A13.0)
[![Build Status](https://github.com/OCA/community-data-files/actions/workflows/test.yml/badge.svg?branch=13.0)](https://github.com/OCA/community-data-files/actions/workflows/test.yml?query=branch%3A13.0)
[![codecov](https://codecov.io/gh/OCA/community-data-files/branch/13.0/graph/badge.svg)](https://codecov.io/gh/OCA/community-data-files)
[![Translation Status](https://translation.odoo-community.org/widgets/community-data-files-13-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/community-data-files-13-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Community Data Files

This project is a collection of Odoo modules containing various data files that are too big to fit the official addons or the other Community projects.

Such data files may include for example tax tables, lists of ZIP codes, official activity nomenclatures...

This project is the continuation of OpenERP-Nomenclatures, which had a narrower scope limited to only official files provided by government agencies.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_payment_unece](account_payment_unece/) | 13.0.1.0.0 |  | UNECE nomenclature for the payment methods
[account_tax_unece](account_tax_unece/) | 13.0.1.0.0 |  | UNECE nomenclature for taxes
[base_bank_from_iban](base_bank_from_iban/) | 13.0.1.0.1 |  | Bank from IBAN
[base_currency_iso_4217](base_currency_iso_4217/) | 13.0.1.0.0 |  | Adds numeric code and full name to currencies, following the ISO 4217 specification
[base_iso3166](base_iso3166/) | 13.0.1.0.1 |  | ISO 3166
[base_unece](base_unece/) | 13.0.1.1.0 | [![astirpe](https://github.com/astirpe.png?size=30px)](https://github.com/astirpe) | Base module for UNECE code lists
[l10n_eu_adr_report](l10n_eu_adr_report/) | 13.0.1.0.1 |  | Print Delivery report to ADR standart
[l10n_eu_product_adr](l10n_eu_product_adr/) | 13.0.2.1.0 |  | Allows to set appropriate danger class and components
[product_fao_fishing](product_fao_fishing/) | 13.0.1.0.0 |  | Set fishing areas and capture technology
[product_meat_unece](product_meat_unece/) | 13.0.1.0.0 |  | This module adds the UNECE Meat Carcasses and Cuts Classification.
[uom_unece](uom_unece/) | 13.0.1.0.0 | [![astirpe](https://github.com/astirpe.png?size=30px)](https://github.com/astirpe) | UNECE nomenclature for the units of measure

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
