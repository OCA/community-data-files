# Copyright 2026 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Migration of NACE Rev. 2 industries to NACE Rev. 2.1, offline.

It runs from the ``18.0.2.0.0`` migration script, and when installing the module
for the NACE Rev. 2 sections that Odoo ships in ``base``.
"""

import csv
import logging
import re
from collections import defaultdict

from odoo import fields
from odoo.osv import expression
from odoo.tools import file_open

_logger = logging.getLogger(__name__)

NACE_CODE = re.compile(r"[A-Z]|\d{2}(\.\d{1,2})?")

# NACE Rev. 2 codes that disappear or get another activity in NACE Rev. 2.1,
# with the NACE Rev. 2.1 code their records are moved to. Taken from the
# official correspondence table (http://data.europa.eu/ux2/nace2/NACE2_NACE2.1);
# codes with several possible targets were solved by hand.
# Any other NACE Rev. 2 code keeps its activity and is reused as is.
NACE2_NACE21 = {
    "K": "L",
    "L": "M",  # ambiguous, chosen by hand
    "M": "N",  # ambiguous, chosen by hand
    "N": "O",  # ambiguous, chosen by hand
    "O": "P",
    "P": "Q",  # ambiguous, chosen by hand
    "Q": "R",
    "R": "S",
    "S": "T",  # ambiguous, chosen by hand
    "T": "U",
    "U": "V",
    "01.49": "01.48",  # ambiguous, chosen by hand
    "01.64": "01.63",
    "14.3": "14.1",
    "14.11": "14.24",
    "14.12": "14.23",
    "14.13": "14.21",  # ambiguous, chosen by hand
    "14.14": "14.22",  # ambiguous, chosen by hand
    "14.19": "14.29",  # ambiguous, chosen by hand
    "14.20": "14.24",
    "14.31": "14.10",
    "14.39": "14.10",
    "16.10": "16.11",  # ambiguous, chosen by hand
    "16.29": "16.28",  # ambiguous, chosen by hand
    "17.29": "17.25",
    "20.51": "20.59",
    "20.52": "20.59",
    "20.53": "20.59",
    "22.19": "22.12",  # ambiguous, chosen by hand
    "22.29": "22.26",  # ambiguous, chosen by hand
    "23.19": "23.15",
    "23.49": "23.45",
    "23.69": "23.66",  # ambiguous, chosen by hand
    "25.3": "25.2",
    "25.4": "25.3",
    "25.5": "25.4",
    "25.6": "25.5",
    "25.7": "25.6",
    "25.29": "25.22",
    "25.30": "25.21",
    "25.40": "25.30",
    "25.50": "25.40",
    "25.61": "25.52",  # ambiguous, chosen by hand
    "25.62": "25.53",
    "25.71": "25.61",
    "25.72": "25.62",
    "25.73": "25.63",
    "26.8": "26.7",
    "26.80": "26.70",
    "28.49": "28.42",  # ambiguous, chosen by hand
    "30.30": "30.31",  # ambiguous, chosen by hand
    "31.01": "31.00",
    "31.02": "31.00",
    "31.03": "31.00",
    "31.09": "31.00",
    "35.12": "35.13",
    "35.13": "35.14",
    "35.14": "35.15",  # ambiguous, chosen by hand
    "38.3": "38.2",  # ambiguous, chosen by hand
    "38.31": "38.21",
    "38.32": "38.21",  # ambiguous, chosen by hand
    "41.1": "68.1",
    "41.2": "41.0",  # ambiguous, chosen by hand
    "41.10": "68.12",
    "41.20": "41.00",  # ambiguous, chosen by hand
    "43.29": "43.24",  # ambiguous, chosen by hand
    "43.39": "43.35",  # ambiguous, chosen by hand
    "43.91": "43.41",
    "45": "47",  # ambiguous, chosen by hand
    "45.1": "47.8",  # ambiguous, chosen by hand
    "45.2": "95.3",
    "45.3": "47.8",  # ambiguous, chosen by hand
    "45.4": "47.8",  # ambiguous, chosen by hand
    "45.11": "47.81",  # ambiguous, chosen by hand
    "45.19": "47.81",  # ambiguous, chosen by hand
    "45.20": "95.31",
    "45.31": "46.72",  # ambiguous, chosen by hand
    "45.32": "47.82",  # ambiguous, chosen by hand
    "45.40": "47.83",  # ambiguous, chosen by hand
    "46.7": "46.8",
    "46.51": "46.50",
    "46.52": "46.50",
    "46.65": "46.47",
    "46.66": "46.50",
    "46.69": "46.64",
    "46.71": "46.81",
    "46.72": "46.82",
    "46.73": "46.83",
    "46.74": "46.84",
    "46.75": "46.85",
    "46.76": "46.86",
    "46.77": "46.87",
    "47.8": "47.1",  # ambiguous, chosen by hand
    "47.19": "47.12",  # ambiguous, chosen by hand
    "47.29": "47.27",  # ambiguous, chosen by hand
    "47.41": "47.40",  # ambiguous, chosen by hand
    "47.42": "47.40",  # ambiguous, chosen by hand
    "47.43": "47.40",  # ambiguous, chosen by hand
    "47.59": "47.55",  # ambiguous, chosen by hand
    "47.63": "47.69",  # ambiguous, chosen by hand
    "47.64": "47.63",  # ambiguous, chosen by hand
    "47.65": "47.64",  # ambiguous, chosen by hand
    "47.81": "47.11",  # ambiguous, chosen by hand
    "47.82": "47.51",  # ambiguous, chosen by hand
    "47.89": "47.12",  # ambiguous, chosen by hand
    "47.99": "47.12",  # ambiguous, chosen by hand
    "49.10": "49.11",  # ambiguous, chosen by hand
    "49.32": "49.33",  # ambiguous, chosen by hand
    "52.29": "52.26",  # ambiguous, chosen by hand
    "56.10": "56.11",  # ambiguous, chosen by hand
    "56.29": "56.22",
    "58.12": "58.19",
    "58.13": "58.12",
    "58.14": "58.13",
    "61.2": "61.1",  # ambiguous, chosen by hand
    "61.3": "61.1",
    "61.20": "61.10",  # ambiguous, chosen by hand
    "61.30": "61.10",
    "62.0": "62.2",  # ambiguous, chosen by hand
    "62.01": "62.10",
    "62.02": "62.20",
    "62.03": "62.20",
    "62.09": "62.90",
    "63.11": "63.10",  # ambiguous, chosen by hand
    "63.12": "63.91",  # ambiguous, chosen by hand
    "63.91": "60.31",
    "63.99": "63.92",
    "64.20": "64.21",
    "64.30": "64.31",  # ambiguous, chosen by hand
    "68.10": "68.11",
    "70.21": "73.30",
    "70.22": "70.20",
    "72.11": "72.10",
    "72.19": "72.10",
    "74.10": "74.14",  # ambiguous, chosen by hand
    "74.90": "74.99",  # ambiguous, chosen by hand
    "77.29": "77.22",
    "78.3": "78.2",
    "78.30": "78.20",
    "80.1": "80.0",
    "80.2": "80.0",
    "80.3": "80.0",
    "80.10": "80.01",
    "80.20": "80.09",
    "80.30": "80.01",
    "81.29": "81.23",
    "82.11": "82.10",
    "82.19": "82.10",  # ambiguous, chosen by hand
    "85.41": "85.33",
    "85.42": "85.40",
    "85.60": "85.69",
    "86.90": "86.99",  # ambiguous, chosen by hand
    "87.90": "87.99",
    "90.0": "90.1",  # ambiguous, chosen by hand
    "90.01": "90.20",
    "90.02": "90.39",
    "90.03": "90.11",  # ambiguous, chosen by hand
    "90.04": "90.31",
    "91.0": "91.1",  # ambiguous, chosen by hand
    "91.01": "91.11",  # ambiguous, chosen by hand
    "91.02": "91.21",
    "91.03": "91.22",
    "91.04": "91.41",  # ambiguous, chosen by hand
    "95.11": "95.10",
    "95.12": "95.10",
    "96.0": "96.9",  # ambiguous, chosen by hand
    "96.01": "96.10",  # ambiguous, chosen by hand
    "96.02": "96.21",  # ambiguous, chosen by hand
    "96.03": "96.30",
    "96.04": "96.23",
    "96.09": "96.99",
}


def read_nace21():
    """Return the NACE Rev. 2.1 rows, parents first: ``{code, parent_code, name,
    nace2_code}``, where ``nace2_code`` is the NACE Rev. 2 code with the same
    activity, if any."""
    with file_open("l10n_eu_nace/data/nace2.1.csv") as csvfile:
        return list(csv.DictReader(csvfile))


def get_industry_fields(env):
    """Return ``{model name: [fields]}`` with the stored fields that point to
    industries, e.g. in partners and CRM leads."""
    industry_fields = defaultdict(list)
    for model_name, model in env.registry.items():
        if (
            model._abstract
            or model._transient
            or not model._auto
            or model_name == "res.partner.industry"
        ):
            continue
        for field in model._fields.values():
            if (
                field.type in ("many2one", "many2many")
                and field.comodel_name == "res.partner.industry"
                and field.store
                and not field.compute
            ):
                industry_fields[model_name].append(field)
    return industry_fields


def move_industry_records(env, old_to_new):
    """Make the records using the industries in ``old_to_new`` (``{old id: new
    id}``) use the new ones instead."""
    if not old_to_new:
        return
    for model_name, model_fields in get_industry_fields(env).items():
        model = (
            env[model_name]
            .sudo()
            .with_context(active_test=False, tracking_disable=True)
        )
        records = model.search(
            expression.OR(
                [[(field.name, "in", list(old_to_new))] for field in model_fields]
            )
        )
        many2one = [f.name for f in model_fields if f.type == "many2one"]
        many2many = [f.name for f in model_fields if f.type == "many2many"]
        for record in records:
            vals = {}
            main_ids = set()
            for name in many2one:
                old_id = record[name].id
                new_id = old_to_new.get(old_id, old_id)
                main_ids.add(new_id)
                if new_id != old_id:
                    vals[name] = new_id
            for name in many2many:
                old_ids = record[name].ids
                # A main industry can't be also secondary
                new_ids = {old_to_new.get(i, i) for i in old_ids} - main_ids
                if new_ids != set(old_ids):
                    vals[name] = [fields.Command.set(list(new_ids))]
            if vals:
                record.write(vals)
        if records:
            _logger.info("Moved %s %s to other industries", len(records), model_name)


def get_code(industry):
    """Return the code at the start of the full name, e.g. ``01.11`` for
    ``01.11 - Growing of cereals...``, if any."""
    full_name = industry.with_context(lang="en_US").full_name or ""
    code = full_name.split(" - ")[0]
    return code if " - " in full_name and NACE_CODE.fullmatch(code) else ""


def migrate_industries(env, rows, correspondence, previous_codes, previous, new):
    """Replace the industries of a previous classification by the new ones.

    :param rows: new industries, parents first, as ``{code, parent_code, name,
        nace2_code}``. ``nace2_code`` is the previous code with the same
        activity, whose industry is reused.
    :param correspondence: ``{previous code: new code}`` for the previous
        codes that disappear or get another activity.
    :param previous_codes: all the codes of the previous classification. Other
        industries are left alone, e.g. the ones of a national classification.
    :param previous: key of the previous classification in ``nace_codes``,
        e.g. ``nace2``.
    :param new: key of the new classification in ``nace_codes``, e.g.
        ``nace21``.

    Parents and targets may be NACE Rev. 2.1 industries, e.g. CNAE 2009 35.15
    goes to NACE 35.12.
    """
    # Don't search archived industries in constraints, e.g. the unique name one
    industry_model = env["res.partner.industry"].sudo().with_context(lang="en_US")
    old = defaultdict(lambda: industry_model)
    for industry in industry_model.with_context(active_test=False).search([]):
        industry = industry.with_context(active_test=True)
        codes = industry.nace_codes or {}
        if "nace21" in codes or new in codes:
            continue
        code = codes.get(previous) or get_code(industry)
        if code in previous_codes:
            if previous not in codes:
                industry.nace_codes = dict(codes, **{previous: code})
            old[code] |= industry
    nace = industry_model._get_nace_map()
    current = industry_model._get_nace_map(new)
    # Reuse the previous industries whose code keeps its activity
    reused = {}
    for row in rows:
        code = row["code"]
        if code not in current and row["nace2_code"] in old:
            candidates = old[row["nace2_code"]].sorted(lambda i: not i.active)
            reused[code] = candidates[:1]
    replaced = industry_model.union(*old.values()) - industry_model.union(
        *reused.values()
    )
    # Archive the rest first, so their names don't clash with the new ones
    archived = replaced.filtered("active")
    archived.action_archive()
    new_map = dict(current)
    created = industry_model
    for row in rows:
        code = row["code"]
        vals = {
            "name": row["name"],
            "full_name": f"{code} - {row['name']}",
            "parent_id": new_map.get(row["parent_code"])
            or nace.get(row["parent_code"], False),
        }
        industry = industry_model.browse(new_map.get(code)) or reused.get(code)
        if industry:
            current_vals = {
                "name": industry.name,
                "full_name": industry.full_name,
                "parent_id": industry.parent_id.id,
            }
            vals = {
                key: value for key, value in vals.items() if current_vals[key] != value
            }
            if code not in current:
                vals["nace_codes"] = dict(industry.nace_codes or {}, **{new: code})
            industry.write(vals)
        else:
            industry = industry_model.create(dict(vals, nace_codes={new: code}))
            created |= industry
        new_map[code] = industry.id
    # Move the records of the replaced industries
    targets = {**nace, **new_map}
    old_to_new = {}
    for industry in replaced:
        code = industry.nace_codes[previous]
        old_to_new[industry.id] = targets[correspondence.get(code, code)]
    move_industry_records(env, old_to_new)
    # And the industries out of the classification that hang from them
    for child in industry_model.search(
        [("parent_id", "in", list(old_to_new)), ("id", "not in", replaced.ids)]
    ):
        child.parent_id = old_to_new[child.parent_id.id]
    _logger.info(
        "%s: %s industries reused, %s created, %s archived",
        new,
        len(reused),
        len(created),
        len(archived),
    )


def migrate_to_nace21(env):
    """Replace the NACE Rev. 2 industries by NACE Rev. 2.1, including the
    sections that Odoo ships in ``base``."""
    rows = read_nace21()
    previous_codes = set(NACE2_NACE21) | {
        row["nace2_code"] for row in rows if row["nace2_code"]
    }
    migrate_industries(env, rows, NACE2_NACE21, previous_codes, "nace2", "nace21")


def post_init_hook(env):
    migrate_to_nace21(env)
