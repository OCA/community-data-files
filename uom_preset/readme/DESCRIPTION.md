This module ships a registry of named **UoM vocabularies** that
translate supplier-specific unit-of-measure codes into Odoo
``uom.uom`` records, by way of UN/CEFACT Recommendation 20 codes.

The registry is intentionally narrow in scope: it covers nomenclatures
that *do not* use UN/CEFACT codes natively. For SCSN-style or any
other Rec 20-conformant supplier flow, callers should look up
``uom.uom.unece_code`` directly via ``uom_unece`` — no preset is
needed.

Two vocabularies ship out of the box:

* ``pricat`` — the Dutch Pricat catalogue/order exchange format,
  sourced verbatim from INDI's public OCI-PunchOut documentation
  (https://www.indi.nl/nl-nl/slim-inkopen/erp-connecties/oci-punchout
  — section *Eenheden-overzicht*).
* ``x12_355`` — ANSI ASC X12 element 355, used in US retail and
  manufacturing EDI. Only the entries where the X12 code differs
  from the UN/CEFACT Rec 20 code are shipped; pass-through entries
  are dropped. Source: *Ariba Network UOM Mapping for ANSI X12*
  (SAP, 2014).

Additional vocabularies can be contributed as small follow-up modules
that inherit the abstract ``uom.preset`` model and extend its
registry.
