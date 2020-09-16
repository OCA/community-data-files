# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("Create res_bank codes")
    cr.execute(
        """
        INSERT INTO res_bank_code (bank_id, code)
        SELECT id, old_code
        FROM res_bank
        WHERE old_code IS NOT NULL
        """
    )
    cr.execute("ALTER TABLE res_bank DROP COLUMN old_code")
