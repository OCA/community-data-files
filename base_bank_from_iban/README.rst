.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==============
Bank from IBAN
==============

This module adds a code to bank definition for using it as matching for filling the bank
from the IBAN bank account number. It uses the existing by country bank mapping in 
standard Odoo (https://github.com/odoo/odoo/blob/12b15cb55414d1f6dfc6b3b4e0c38638551ee54d/addons/base_iban/models/res_partner_bank.py#L81-L149),
taken from ISO 3166-1 -> IBAN template, as described here:
http://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country

Configuration
=============

#. Go to *Contacts > Configuration > Bank Accounts > Banks*.
#. Create or modify a bank.
#. Put the corresponding code for that bank in the field "Code".

Usage
=====

To use this module, you need to:

#. Go to Partner
#. Click *Bank Account(s)* in "Sales & Purchases" page.
#. Create/modify IBAN bank account.
#. When you put the bank account number, module extracts bank digits from the format of the country, and try to match an existing bank by country and code.
#. If there's a match, the bank is selected automatically.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/110/11.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/community-data-files/issues>`_.
In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Carlos Dauden <carlos.dauden@tecnativa.com>


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
