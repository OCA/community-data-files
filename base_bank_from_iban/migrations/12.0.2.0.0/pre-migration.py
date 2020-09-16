# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Save bank code")
    cr.execute(
        "ALTER TABLE res_bank ADD COLUMN IF NOT EXISTS old_code VARCHAR(255)"
    )
    cr.execute("UPDATE res_bank SET old_code=code")
