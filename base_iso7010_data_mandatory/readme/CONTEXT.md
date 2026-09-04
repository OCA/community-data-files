While the `base_iso7010` module provides the structure to manage safety symbols, it doesn't contain any actual symbols by default. A common business need is to have the standard set of ISO 7010 "Mandatory Action" symbols (the blue circle signs indicating required actions, often related to PPE) readily available within Odoo without requiring manual data entry for each one. These are frequently used symbols for indicating requirements like wearing gloves, eye protection, hearing protection, safety footwear, etc.

This module fulfills the need for readily available, standard mandatory symbols for selection and use in various Odoo processes.

*Example Use Case:* After installing `base_iso7010`, a user wants to link the "Wear Protective Gloves" symbol (M009) to a specific Work Center using the `mrp_workcenter_safety_symbol` module. Installing `base_iso7010_data_mandatory` makes the M009 record available for selection.
