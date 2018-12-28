# Copyright 2011 Numérigraphe SARL.
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class PartnerCategory(models.Model):
    """Let users search on code without a dot"""
    _inherit = 'res.partner.category'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """When no results are found, try again with an additional "."."""
        results = super(PartnerCategory, self).name_search(
            name, args=args, operator=operator, limit=limit)
        if not results and name and len(name) > 2:
            # Add a "." after the 2nd character, in case that makes a NACE code
            results = super(PartnerCategory, self).name_search(
                '%s.%s' % (name[:2], name[2:]), args=args, operator=operator,
                limit=limit)
        return results
