# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class UomPreset(models.AbstractModel):
    """Vocabulary registry for non-UN/CEFACT supplier UoM codes.

    A *vocabulary* is a named mapping from supplier-specific UoM codes
    to UN/CEFACT Recommendation 20 codes (the codes shipped by
    ``uom_unece``). Resolution always goes through ``uom.uom.unece_code``,
    so adding a new vocabulary never requires shipping new ``uom.uom``
    records.

    This module is intentionally narrow: it covers the supplier
    nomenclatures that *do not* use UN/CEFACT codes natively. For
    SCSN-style or any other Rec 20-conformant supplier, callers should
    look up ``uom.uom.unece_code`` directly — no preset is needed.

    To add a vocabulary, inherit this model and extend both
    :meth:`_uom_preset_vocabularies` and :meth:`_uom_preset_selection`.
    """

    _name = "uom.preset"
    _description = "UoM Preset (Vocabulary Registry)"

    @api.model
    def _uom_preset_vocabularies(self):
        """Return ``{vocab_key: {alias_upper: unece_code}}``.

        ``alias_upper`` keys must be uppercase. ``unece_code`` values
        must be valid UN/CEFACT Rec 20 codes that ``uom_unece`` has
        attached to a ``uom.uom`` record.
        """
        return {
            # Pricat (catalogue/order exchange format used in Dutch B2B
            # technical wholesale, mirrored on INDI's OCI documentation
            # at https://www.indi.nl/nl-nl/slim-inkopen/erp-connecties/
            # oci-punchout — section "Eenheden-overzicht").
            "pricat": {
                "STU": "C62",  # Stuks
                "PAK": "C62",  # Verpakking
                "DOO": "C62",  # Doos
                "SET": "C62",  # Set
                "PAA": "C62",  # Paar
                "ROL": "C62",  # Rol
                "DRU": "C62",  # Vat
                "KIT": "C62",  # Set / kit
                # Pricat MTR/KGM/LTR are intentionally omitted — they
                # are already valid UN/CEFACT Rec 20 codes, so callers
                # resolve them via ``uom_unece`` directly.
            },
            # ANSI ASC X12 element 355 (US retail/manufacturing EDI).
            # Only entries where the ANSI X12 code differs from the
            # UN/CEFACT Rec 20 code — pass-through entries are dropped
            # so callers fall through to ``uom_unece`` directly. Source:
            # "Ariba Network UOM Mapping for ANSI X12" (SAP, 2014,
            # https://help.sap.com/doc/ba35b82316194c94961cfabb0284e988/
            # cloud/en-US/uomMappingForANSI_X12Documents.pdf).
            "x12_355": {
                "03": "SEC",  # SECONDS
                "04": "06",  # SMALL SPRAY
                "12": "PA",  # PACKET
                "3F": "B35",  # KILOGRAMS PER LITER OF PRODUCT
                "4D": "CUR",  # CURIE
                "4I": "MTS",  # METERS PER SECOND
                "4J": "MSK",  # METERS PER SECOND PER SECOND
                "4S": "PAL",  # PASCAL
                "4V": "MQH",  # CUBIC METER PER HOUR
                "65": "COU",  # COULOMB
                "67": "SIE",  # SIEMENS
                "70": "VLT",  # VOLT
                "79": "A53",  # ELECTRON VOLT
                "82": "OHM",  # OHM
                "83": "FAR",  # FARAD
                "86": "JOU",  # JOULES
                "A8": "D67",  # DOLLARS PER HOURS
                "AC": "ACR",  # ACRE
                "AF": "CGM",  # CENTIGRAM
                "AT": "ATM",  # ATMOSPHERE
                "B8": "BD",  # BOARD
                "BA": "BL",  # BALE
                "BC": "BJ",  # BUCKET
                "BD": "BE",  # BUNDLE
                "BE": "D79",  # BEAM
                "BF": "BFT",  # BOARD FEET
                "BI": "BR",  # BAR
                "BJ": "D92",  # BAND
                "BK": "D63",  # BOOK
                "BL": "D64",  # BLOCK
                "BM": "BT",  # BOLT
                "BN": "VQ",  # BULK
                "BQ": "BHP",  # BRAKE HORSE POWER
                "BR": "BLL",  # BARREL
                "BS": "BK",  # BASKET
                "BT": "E2",  # BELT
                "BU": "BUA",  # BUSHEL
                "BV": "BUI",  # BUSHEL, DRY IMPERIAL
                "BY": "BTU",  # BRITISH THERMAL UNIT (BTU)
                "C3": "CLT",  # CENTILITER
                "C8": "DMQ",  # CUBIC DECIMETER
                "CA": "CS",  # CASE
                "CB": "CO",  # CARBOY
                "CC": "CMQ",  # CUBIC CENTIMETER
                "CF": "FTQ",  # CUBIC FEET
                "CI": "INQ",  # CUBIC INCHES
                "CL": "CY",  # CYLINDER
                "CM": "CMT",  # CENTIMETER
                "CN": "CA",  # CAN
                "CO": "D90",  # CUBIC METERS (NET)
                "CP": "CR",  # CRATE
                "CR": "MTQ",  # CUBIC METER
                "CS": "D66",  # CASSETTE
                "CW": "CWA",  # HUNDRED POUNDS (CWT)
                "CX": "CL",  # COIL
                "CY": "YDQ",  # CUBIC YARD
                "D3": "DMK",  # SQUARE DECIMETER
                "DA": "DAY",  # DAYS
                "DF": "DRA",  # DRAM
                "DK": "KMT",  # KILOMETERS
                "DL": "DLT",  # DECILITER
                "DM": "DMT",  # DECIMETER
                "DP": "DPR",  # DOZEN PAIR
                "DZ": "DZN",  # DOZEN
                "FA": "FAH",  # FAHRENHEIT
                "FO": "OZA",  # FLUID OUNCE
                "FT": "FOT",  # FOOT
                "FZ": "OZI",  # FLUID OUNCE (IMPERIAL)
                "G4": "GBQ",  # GIGABECQUEREL
                "G5": "GII",  # GILL (IMPERIAL)
                "GA": "GLL",  # GALLON
                "GG": "GGR",  # GREAT GROSS (DOZEN GROSS)
                "GI": "GLI",  # IMPERIAL GALLONS
                "GR": "GRM",  # GRAM
                "GS": "GRO",  # GROSS
                "GT": "E4",  # GROSS KILOGRAM
                "GX": "GRN",  # GRAIN
                "H4": "HLT",  # HECTOLITER
                "HB": "HBX",  # HUNDRED BOXES
                "HG": "HGM",  # HECTOGRAM
                "HR": "HUR",  # HOURS
                "HU": "CEN",  # HUNDRED
                "HW": "CWI",  # HUNDRED WEIGHT (LONG)
                "HZ": "HTZ",  # HERTZ
                "IN": "INH",  # INCH
                "JG": "D95",  # JOULE PER GRAM
                "JU": "JG",  # JUG
                "K4": "KVA",  # KILOVOLT AMPERES
                "K7": "KWT",  # KILOWATT
                "KC": "KMQ",  # KILOGRAMS PER CUBIC METER
                "KE": "KG",  # KEG
                "KG": "KGM",  # KILOGRAM
                "KH": "KWH",  # KILOWATT HOUR
                "KP": "KMH",  # KILOMETERS PER HOUR
                "KQ": "KPA",  # KILOPASCAL
                "KV": "KEL",  # KELVIN
                "LB": "LBR",  # POUND
                "LG": "LTN",  # LONG TON
                "LQ": "LD",  # LITERS PER DAY
                "LT": "LTR",  # LITER
                "M3": "MT",  # MAT
                "M8": "MPA",  # MEGA PASCALS
                "ME": "MGM",  # MILLIGRAM
                "MJ": "MIN",  # MINUTES
                "ML": "MLT",  # MILLILITER
                "MM": "MMT",  # MILLIMETER
                "MN": "NT",  # METRIC NET TON
                "MO": "MON",  # MONTHS
                "MP": "TNE",  # METRIC TON
                "MR": "MTR",  # METER
                "MS": "MMK",  # SQUARE MILLIMETER
                "MT": "E5",  # METRIC LONG TON
                "MU": "MCU",  # MILLICURIE
                "N4": "D23",  # PEN GRAMS (PROTEIN)
                "N6": "MHZ",  # MEGAHERTZ
                "NM": "NMI",  # NAUTICAL MILE
                "NT": "E3",  # TRAILER
                "NW": "NEW",  # NEWTON
                "PA": "PL",  # PAIL
                "PC": "C62",  # UNIT
                "PG": "D96",  # POUNDS GROSS
                "PJ": "LBR",  # POUND
                "PL": "D97",  # PALLET/UNIT LOAD
                "PP": "PG",  # PLATE
                "PU": "D98",  # MASS POUNDS
                "PX": "PTI",  # PINT, IMPERIAL
                "Q1": "QAN",  # QUARTER (TIME)
                "Q2": "PTD",  # PINT U.S. DRY
                "QS": "QTD",  # QUART, DRY U.S.
                "R2": "BQL",  # BECQUEREL
                "R3": "RPM",  # REVOLUTIONS PER MINUTE
                "RE": "RL",  # REEL
                "RL": "RO",  # ROLL
                "RO": "D65",  # ROUND
                "S9": "SL",  # SLIP SHEET
                "SA": "D7",  # SANDWICH
                "SB": "MIK",  # SQUARE MILE
                "SC": "CMK",  # SQUARE CENTIMETER
                "SF": "FTK",  # SQUARE FOOT
                "SH": "ST",  # SHEET
                "SI": "INK",  # SQUARE INCH
                "SJ": "SA",  # SACK
                "SL": "D99",  # SLEEVE
                "SM": "MTK",  # SQUARE METER
                "ST": "SET",  # SET
                "T9": "MWH",  # THOUSAND KILOWATT HOURS
                "TB": "TU",  # TUBE
                "TG": "GT",  # GROSS TON
                "TH": "MIL",  # THOUSAND
                "TM": "MBF",  # THOUSAND FEET (BOARD)
                "TN": "STN",  # NET TON (2,000 LB).
                "TO": "APZ",  # TROY OUNCE
                "TU": "D14",  # THOUSAND LINEAR YARDS
                "TX": "LBT",  # TROY POUND
                "TY": "PU",  # TRAY
                "UN": "C62",  # UNIT
                "WK": "WEE",  # WEEK
                "WP": "DWT",  # PENNYWEIGHT
                "YD": "YRD",  # YARD
                "YR": "ANN",  # YEARS
            },
        }

    @api.model
    def _uom_preset_selection(self):
        """Return ``[(vocab_key, label)]`` for use as a Selection field."""
        return [
            ("pricat", self.env._("Pricat (catalogue exchange format)")),
            ("x12_355", self.env._("ANSI X12 element 355 (US EDI)")),
        ]

    @api.model
    def _resolve(self, vocabulary, supplier_code):
        """Translate ``supplier_code`` via ``vocabulary`` to a ``uom.uom``.

        Strict lookup: returns an empty recordset when the vocabulary is
        unknown, or when the code is not registered in that vocabulary.
        Callers handle their own fallback chain (UN/CEFACT lookup, name
        match, default UoM, …).
        """
        UomUom = self.env["uom.uom"]
        unece_code = None
        if vocabulary and supplier_code:
            vocab = self._uom_preset_vocabularies().get(vocabulary)
            if vocab:
                unece_code = vocab.get(supplier_code.strip().upper())
        if not unece_code:
            return UomUom.browse()
        return UomUom.search([("unece_code", "=", unece_code)], limit=1)
