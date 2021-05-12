# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SeatekContactCode(models.Model):
    _inherit = 'res.partner'

    contact_code = fields.Char(string='Contact Code', copy=False)