# -*- coding: utf-8 -*-
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2017  Creu Blanca <www.creublanca.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

try:
    import pycountry
except ImportError:
    pass


class ResCountry(models.Model):
    _inherit = 'res.country'

    code_alpha3 = fields.Char(
        string='Country Code (3-letter)', size=3, store=True,
        help='ISO 3166-1 alpha-3 (three-letter) code for the country',
        compute="_compute_codes")
    code_numeric = fields.Char(
        string='Country Code (numeric)', size=3, store=True,
        help='ISO 3166-1 numeric code for the country',
        compute="_compute_codes")

    @api.multi
    @api.depends('code')
    def _compute_codes(self):
        for country in self:
            try:
                try:
                    c = pycountry.countries.get(alpha_2=country.code)
                except KeyError:
                    c = pycountry.countries.get(alpha2=country.code)
                country.code_alpha3 = getattr(c, 'alpha_3',
                                              getattr(c, 'alpha3', False))
                country.code_numeric = c.numeric
            except KeyError:
                try:
                    try:
                        c = pycountry.historic_countries.get(
                            alpha_2=country.code)
                    except KeyError:
                        c = pycountry.historic_countries.get(
                            alpha2=country.code)
                    country.code_alpha3 = getattr(c, 'alpha_3',
                                                  getattr(c, 'alpha3', False))
                    country.code_numeric = c.numeric
                except KeyError:
                    country.code_alpha3 = False
                    country.code_numeric = False
