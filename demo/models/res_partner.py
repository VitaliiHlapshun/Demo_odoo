# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    rent_ids = fields.One2many('library.book.rent', 'borrower_id')
