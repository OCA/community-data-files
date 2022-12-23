This module adds a code to bank definition for using it as matching for filling the bank
from the IBAN bank account number. It uses the existing by country bank mapping in
standard Odoo (https://github.com/odoo/odoo/blob/f5ffcf7feec5526a483f8ddd240648c084351008/addons/base_iban/models/res_partner_bank.py#L105-L175),
taken from ISO 3166-1 -> IBAN template, as described here:
http://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country
