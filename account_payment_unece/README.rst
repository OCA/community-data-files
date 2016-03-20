.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Account Payment UNECE
=====================

This module adds a field *UNECE Payment Mean* on *Payment Mode Types* to be able to use a standard written by the `United Nations Economic Commission for Europe <http://www.unece.org>`_ (which has 56 members states in Europe, America and Central Asia, cf `Wikipedia <https://en.wikipedia.org/wiki/United_Nations_Economic_Commission_for_Europe>`_). This standard define a codification of the payment modes, cf the `official code list <http://www.unece.org/trade/untdid/d99b/tred/tred4461.htm>`_.

This codification is used for example in the two main international standards for electronic invoicing:

* `Cross Industry Invoice <http://tfig.unece.org/contents/cross-industry-invoice-cii.htm>`_ (CII),
* `Universal Business Language <http://ubl.xml.org/>`_ (UBL)

Configuration
=============

Go to the menu *Accounting > Configuration > Miscellaneous > Payment Export Types* and select the appropriate value for the *UNECE Code*.

Usage
=====


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/101/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/community-data-files/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
community-data-files/issues/new?body=module:%20
account_payment_unece%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

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
