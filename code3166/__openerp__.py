# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2009 Alejandro Sanchez (http://www.asr-oss.com)
#                       Alejandro Sanchez <alejandro@asr-oss.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the Affero GNU General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the Affero GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "ISO 3166-1 codes for countries",
    "version": "8.0.1.0.0",
    "author": "ASR-OSS, "
              "FactorLibre, "
              "Tecon, "
              "Pexego, "
              "Malagatic, "
              "Comunitea, "
              "Binovo IT Human Project"
              "Odoo Community Association (OCA)",
    "category": "",
    "website": "",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "views/country_view.xml",
        "data/data_res_country.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
}
