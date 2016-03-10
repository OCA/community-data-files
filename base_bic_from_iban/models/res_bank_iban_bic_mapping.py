# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import re
from openerp import api, fields, models


class ResBankIbanBicMapping(models.Model):
    _name = 'res.bank.iban.bic.mapping'
    _description = 'Map IBANs to BICs'
    _rec_name = 'bic'

    match_type = fields.Selection(
        [('regex', 'Regex')], string='Matching type', required=True)
    country_id = fields.Many2one(
        'res.country', string='Country', required=True)
    data = fields.Serialized(
        'Data', help='The semantics of this field depends on the matching '
        'type chosen. Possibilities are:\n'
        '- a regex matching the BBAN (IBAN with the first four characters '
        'removed)')
    bic = fields.Char('BIC', size=11, required=True)

    @api.model
    def lookup_bic(self, iban):
        """Return a BIC or None if not found"""
        if not iban:
            return None
        country_code = iban[:2].upper()
        # if there's a specialized function for the country, use that
        if hasattr(self, 'lookup_bic_%s' % country_code):
            return getattr(self, 'lookup_bic_%s' % country_code)(iban)
        country = self.env['res.country'].search([
            ('code', '=ilike', country_code),
        ])
        for mapping in self.search([('country_id', '=', country.id)]):
            if mapping.match(iban):
                return mapping.bic

    @api.multi
    def match(self, iban):
        """Return True if this mapping matches a given IBAN"""
        self.ensure_one()
        return getattr(self, '_match_%s' % self.match_type)(iban)

    @api.multi
    def _match_regex(self, iban):
        """Match the regex against the IBAN's BBAN"""
        return re.match(self.data, iban[4:])
