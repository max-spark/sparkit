# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Country(models.Model):
    _name = 'res.country'
    _inherit = 'res.country'

    is_active = fields.Boolean(string="Partnerships within Country?")
    community_ids = fields.One2many('sparkit.community', 'country_id',
        string="Communities")
    num_ppl_per_household = fields.Float(string="Average Number of People Per Household")
