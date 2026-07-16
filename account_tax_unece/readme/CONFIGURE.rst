#. Go to the menu *Accounting > Configuration > Accounting > Taxes*
#. Set the field *UNECE Type Code* (the value should be *VAT* for most of your
   taxes).
#. Set the field *UNECE Category Code*.
#. On VAT taxes whose UNECE Category Code is neither *S* (standard rate) nor
   *Z* (zero rated), set the field *VAT Exemption Reason* (VATEX): it carries
   the reason why the transaction is exempted from VAT. For the categories *K*
   (intra-community supply) and *G* (export), it is set automatically.

There are localization modules that fill this information for specific chart
of accounts, so this step shouldn't be needed if installed.
