# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    company_type = fields.Selection([
		('community_member', 'Community Member'),
		('person', 'Individual (Non-Community Member)'),
		('company', 'Company'),
		('community_leader', 'Community Leader'),
		('boda_moto', 'Boda/Moto'),
        ('community_facilitator', 'Community Facilitator')
		], select=True, string="Contact Type")

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
        ], select=True, string="Gender")

    community_id = fields.Many2one('sparkit.community', string="Community")
    new_leader = fields.Selection([('1', 'Yes'), ('0', 'No')],
        select=True, string="New Leader",
        help="Tick this box if the leader has never been in a leadership before.")
