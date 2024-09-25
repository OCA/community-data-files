On the product form, you can mark a product as dangerous. That will
enable a new tab on the product form's notebook on which you can select
the dangerous goods that applies to this particular product, out of a
list of dangerous goods that represents Table A from chapter 3 of the
ADR specifications document.

It is possible to specify a different, or no goods per product variant.

The data in this module is generated based on a spreadsheet from
<https://cepa.be>. This spreadsheet, just like the specifications
themselves sometimes contain multiple options for each dangerous good,
or additional restrictions that apply. That complexity is not encoded in
the data in this module. For each dangerous goods that you configure on
the products in your database, you should verify the correctness of the
data against the latest version of the specifications and in case of
additional restrictions or multiple options for the dangerous goods you
should configure the goods according to the situation in your warehouse.
You can access the configuration of the dangerous goods using menu
*Inventory -\> Configuration -\> Dangerous Goods*.

The number of ADR points on the picking is based on the product weight
field if it is filled in, or otherwise on the UoM quantity in the
product's reference UoM (presumably Liter or Kilogram).

This module defines an ADR user group and an ADR admin group. Membership
of one of these groups is required to access the product tab with the
ADR info. By default, all inventory users are added to the ADR user
group.
