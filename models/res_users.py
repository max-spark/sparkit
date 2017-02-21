# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    fac_community_ids = fields.One2many('sparkit.community', 'facilitator_id',
        string="Facilitated Communities")
    cofac_community_ids = fields.One2many('sparkit.community', 'co_facilitator_id',
        string="Co-Facilitated Communities")
    pm_community_ids = fields.One2many('sparkit.community', 'program_manager_id',
        string="Managed Communities")
