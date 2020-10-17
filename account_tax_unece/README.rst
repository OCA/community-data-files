.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Account UNECE
=============

This module adds two fields *UNECE Type Code* and *UNECE Category Code* on taxes to allow the use of the standards written by the `United Nations Economic Commission for Europe <http://www.unece.org>`_ (which has 56 members states in Europe, America and Central Asia, cf `Wikipedia <https://en.wikipedia.org/wiki/United_Nations_Economic_Commission_for_Europe>`_):

* the UNECE Tax Type code is defined in the `DataElement 5153 <http://www.unece.org/trade/untdid/d97b/uncl/uncl5153.htm>`_,
* the UNECE Tax Category Code is defined in the `DataElement 5305 <http://www.unece.org/trade/untdid/d97a/uncl/uncl5305.htm>`_.

This codification is part of the UNCL (United Nations Code List). This codification is used for example in the two main international standards for electronic invoicing:

* `Cross Industry Invoice <http://tfig.unece.org/contents/cross-industry-invoice-cii.htm>`_ (CII),
* `Universal Business Language <http://ubl.xml.org/>`_ (UBL).

Configuration
=============

Go to the menu *Accounting > Configuration > Accounting > Taxes* and configure the *UNECE Type Code* (the value should be *VAT* for most of your taxes) and the *UNECE Category Code*.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/101/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/community-data-files/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
