This module adds a code to bank definition and fills the bank of a bank
account from its IBAN.

When a bank account is saved, the bank data (name, BIC and bank code)
is taken from the [schwifty](https://github.com/mdomke/schwifty) bank
registry. If no bank with that code exists for the country, it is
created. An existing bank only gets its empty fields completed.
