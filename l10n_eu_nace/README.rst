.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

European NACE partner categories
================================

This module imports the NACE rev. 2 classification
categories as partner categories in 23 languages, courtesy of the EU.

The *Statistical Classification of Economic Activities in the European Community*
commonly referred to as NACE, is a European industry standard classification
system using a 6 digit code.
NACE is equivalent to the SIC and NAICS system:
* Standard Industrial Classification
* North American Industry Classification System.

This module is a rewrite of the older community module "partner_nace" from
the former `extra-addons` repository of Odoo v5 (called OpenERP at the time).

Usage
=====
Each NACE code is represented by a partner category.
Once this module is installed, you can assign NACE categories to your partners
by simply adding the corresponding category in the partner's form.

Obtaining updated data
======================
The data imported into OpenERP is generated from the files downloaded
from the RAMON service::

    http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_CLS_DLD&StrNom=NACE_REV2&StrLanguageCode=FR&StrLayoutCode=#

If you want to update the data or add another translation, download the
corresponding file from RAMON in CSV format, using ',' as a separator.
Save it to the directory "data" and name it according to the language
code::

    NACE_REV2_<language code>.csv
Then update the LANGS constant in the script "make_data.py" and run it to
refresh the OpenERP data files. Finally, upgrade the module to load the data.

Credits
=======

Contributors
------------

* Lionel Sausin (Numérigraphe) <ls@numerigraphe.com>
* Sistheo
* data files courtesy of the European Union

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.



