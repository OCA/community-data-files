# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Numérigraphe SARL.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api


class PartnerCategory(models.Model):
    """Let users search on code without a dot"""
    _inherit = 'res.partner.category'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """When no results are found, try again with an additional "."."""
        results = super(PartnerCategory, self).name_search(name, args=args,
            operator=operator, limit=limit)
        if not results and name and len(name) > 2:
            # Add a "." after the 2nd character, in case that makes a NACE code
            results = super(PartnerCategory, self).name_search(
                '%s.%s' % (name[:2], name[2:]), args=args, operator=operator,
                limit=limit)
        return results
