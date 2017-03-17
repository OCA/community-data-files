# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class UneceCodeList(models.Model):
    _inherit = 'unece.code.list'

    type = fields.Selection(selection_add=[
        ('payment_means', 'Payment Means (UNCL 4461)')])
