#!/usr/bin/env python3
# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=print-used
"""Generate US ECCN codes CSV from manual input.

Since the US Export Administration Regulations don't provide a simple
API or data export, US codes are typically added manually by maintainers
who reference the official eCFR Part 774.

This script helps generate properly formatted CSV entries.
"""

import csv
import sys

# Define common US ECCN codes
# Source: https://www.ecfr.gov/current/title-15/part-774
US_CODES = [
    ("EAR99", "Items not otherwise specified - Low-level controls"),
    ("0A001", "Nuclear reactors and specially designed equipment"),
    ("1C010", "Fibrous or filamentary materials (carbon, glass, aramid)"),
    ("3A001", "Electronic components and specially designed components"),
    ("3A002", "General purpose electronic equipment"),
    ("3A991", "Electronic devices not controlled by 3A001"),
    ("3A992", "General purpose electronic equipment"),
    ("4A003", "Digital computers and related equipment"),
    ("4A994", "Computers not controlled by 4A003"),
    ("4D994", "Software for computers"),
    ("5A002", "Information security systems and equipment"),
    ("5A992", "Telecommunications equipment"),
    ("5D002", "Software for information security"),
    ("5D992", "Software for telecommunications"),
    ("6A003", "Cameras and optical sensors"),
    ("6A993", "Cameras and equipment"),
    ("7A003", "Inertial navigation systems and components"),
    ("7A994", "Navigation equipment"),
    ("8A002", "Marine systems and equipment"),
    ("9A004", "Airborne equipment"),
    ("9A991", "Aircraft and related equipment"),
]


def generate_us_csv(output_file="../data/trade_compliance_code_us.csv"):
    """Generate US codes CSV file."""
    print(f"Generating US ECCN codes CSV to {output_file}...")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["id", "name", "regime_id/id", "description"])

        # Write US codes
        for code, description in US_CODES:
            xml_id = f"compliance_code_us_{code.lower().replace('-', '_')}"
            writer.writerow(
                [
                    xml_id,
                    code,
                    "product_trade_compliance.regime_us_ear",
                    description,
                ]
            )

    print(f"✓ Generated {len(US_CODES)} US ECCN codes")
    print(f"  Output: {output_file}")
    print("\nTo add more codes:")
    print("1. Edit US_CODES list in this script")
    print('2. Add entries: ("CODE", "Description")')
    print("3. Re-run this script")
    print("4. Merge the output with the main CSV file")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_us_csv(sys.argv[1])
    else:
        generate_us_csv()
