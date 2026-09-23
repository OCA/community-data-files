# Trade Compliance Data Scripts

Scripts for refreshing compliance code data from official sources.

> **Note**: The module includes 2,672 pre-generated codes. These scripts are for
> maintainers updating data when regulations change.

## Available Scripts

### 1. EU Dual-Use Codes: `convert_excel_to_csv.py`

Converts official EU Excel file to CSV format.

**Source**:
https://policy.trade.ec.europa.eu/help-exporters-and-importers/exporting-dual-use-items_en

**Usage**:

```bash
# 1. Download Excel from EU official source
# 2. Save in scripts/ directory (replace existing file)
cd product_trade_compliance/scripts
python3 convert_excel_to_csv.py
```

**Output**: `../data/trade_compliance_code_eu.csv` (2,652 codes)

**When to update**: When EU publishes new Dual-Use Regulation amendments

### 2. US ECCN Codes: `generate_us_codes.py`

Generates US Export Control Classification Numbers (ECCN) from curated list.

**Source**: https://www.ecfr.gov/current/title-15/part-774 (manual curation)

**Usage**:

```bash
cd product_trade_compliance/scripts
python3 generate_us_codes.py
```

**Output**: `../data/trade_compliance_code_us.csv` (21 common codes)

**To add more codes**:

1. Edit `US_CODES` list in `generate_us_codes.py`
2. Add entries: `("CODE", "Description")`
3. Re-run script
4. Merge output with main CSV file

**When to update**: When new ECCN codes are added to Commerce Control List

## Combining Generated CSVs

After running both scripts, combine into the single module CSV:

```bash
cd product_trade_compliance/scripts

# Generate both files
python3 generate_us_codes.py
python3 convert_excel_to_csv.py

# Combine into main CSV (US codes first, then EU codes, skip duplicate headers)
cat ../data/trade_compliance_code_us.csv > ../data/trade.compliance.code.csv
tail -n +2 ../data/trade_compliance_code_eu.csv >> ../data/trade.compliance.code.csv

# Remove duplicates if any
awk -F',' 'NR==1 || !seen[$2,$3]++' ../data/trade.compliance.code.csv > temp.csv
mv temp.csv ../data/trade.compliance.code.csv
```

## After Updating Data

1. **Test the module**:

   ```bash
   odoo --test-enable --init product_trade_compliance --stop-after-init
   ```

2. **Verify data loaded**:

   - Check Inventory → Configuration → Trade Compliance → Compliance Codes
   - Verify count matches expected

3. **Update this README**: Update "Last Updated" dates below

4. **Commit changes**:

   ```bash
   git add data/ scripts/
   git commit -m "[REF] product_trade_compliance: Update compliance codes"
   ```

5. **Create Pull Request** to OCA

## Official Data Sources

### EU Dual-Use Regulation

- **URL**:
  https://policy.trade.ec.europa.eu/help-exporters-and-importers/exporting-dual-use-items_en
- **Download**:
  [Excel File](https://circabc.europa.eu/ui/group/654251c7-f897-4098-afc3-6eb39477797e/library/19eee88d-8b29-40a0-9e02-a662ecafaf6e/details?download=true)
- **Regulation**: (EU) 2021/821
- **Last Updated**: September 2024 (2,652 codes)

### US Export Administration Regulations

- **URL**: https://www.ecfr.gov/current/title-15/part-774
- **Document**: Commerce Control List (CCL)
- **Agency**: Bureau of Industry and Security
- **Last Updated**: Initial release (21 common codes)

## Requirements

```bash
pip install openpyxl  # For EU Excel parsing
```

## Troubleshooting

### openpyxl not found

```bash
pip install openpyxl
```

### Excel file not found

Ensure the Excel filename in `convert_excel_to_csv.py` matches the downloaded file
exactly.

### CSV format issues

If EU changes Excel structure, update column indices in `convert_excel_to_csv.py`:

- `id_idx = headers.index('ID')`
- `code_idx = headers.index('CODE')`
- `label_idx = headers.index('LABEL')`

### Duplicate codes

The combine command includes deduplication by (name, regime_id). If duplicates persist,
check for data quality issues in source files.

## Data Format

Single CSV file: `data/trade.compliance.code.csv`

```csv
id,name,regime_id/id,description
compliance_code_us_ear99,EAR99,product_trade_compliance.regime_us_ear,Items not otherwise specified
compliance_code_eu_223001,0,product_trade_compliance.regime_eu_dual,CATEGORY 0 - NUCLEAR MATERIALS
```

**Fields**:

- `id`: Unique XML ID (prefix: `compliance_code_us_` or `compliance_code_eu_`)
- `name`: Compliance code (e.g., "3A001", "EAR99")
- `regime_id/id`: Regime reference (`regime_us_ear` or `regime_eu_dual`)
- `description`: Human-readable description
