This module adds a code to bank definition for using it as matching for filling the bank
from the IBAN bank account number. It uses the existing by country bank mapping in
standard Odoo (https://github.com/odoo/odoo/blob/12b15cb55414d1f6dfc6b3b4e0c38638551ee54d/addons/base_iban/models/res_partner_bank.py#L81-L149),
taken from ISO 3166-1 -> IBAN template, as described here:
http://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country
