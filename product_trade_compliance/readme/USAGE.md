**Configuration:**

1. Navigate to **Inventory > Configuration > Trade Compliance > Regimes**
   to view the available compliance regimes (US-EAR, EU-DUAL).

2. Navigate to **Inventory > Configuration > Trade Compliance > Compliance Codes**
   to create and manage compliance codes.

3. (Optional) Set default compliance codes on product categories:
   - Go to **Inventory > Configuration > Product Categories**
   - Edit a category and set the **Default Compliance Code** field
   - All new products created in this category will automatically inherit this code

**Product Configuration:**

1. Open any product from **Inventory > Products**

2. Go to the **Trade Compliance** tab

3. Set the **Compliance Code** field to the appropriate code

4. The **Compliance Regime** and **Code Description** fields will automatically
   display information from the selected code

**Automatic Code Inheritance:**

When creating a new product, if the product category has a default compliance
code set, the product will automatically inherit this code. This inheritance
only happens when:

- Creating a new product, OR
- Changing the category when the product has no compliance code set

If a product already has a compliance code, changing its category will NOT
override the existing code.

**Included Data:**

The module includes 2,672 pre-generated compliance codes:
- **EU**: 2,652 codes from EU Dual-Use Regulation (EU) 2021/821 (September 2024)  
- **US**: 21 common ECCN codes from Commerce Control List

Data loads automatically on module installation.

**Refreshing Data (Maintainers):**

The `scripts/` directory contains tools to refresh data from official sources:

- **EU codes**: `python3 scripts/convert_excel_to_csv.py` (converts Excel to CSV)
- **US codes**: `python3 scripts/generate_us_codes.py` (generates from curated list)

After running scripts, combine CSVs and test. See `scripts/README.md` for detailed workflow.

**Official Sources:**
- **EU**: https://policy.trade.ec.europa.eu/help-exporters-and-importers/exporting-dual-use-items_en
- **US**: https://www.ecfr.gov/current/title-15/part-774
