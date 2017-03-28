# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    company_type = fields.Selection([
		('community_member', 'Community Member'),
		('person', 'Individual (Non-Community Member)'),
		('company', 'Company/NGO/CSO/Government'),
		('community_leader', 'Community Leader'),
		('boda_moto', 'Boda/Moto'),
        ('community_facilitator', 'Community Facilitator'),
        ('technical_advisor', 'Technical Advisor'),
        ('donor', 'Donor'),
		], select=True, string="Contact Type",
        help="Please select the category that bests represents this contact.",
        track_visibility='onchange')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
        ], select=True, string="Gender",
        track_visibility='onchange')

    lang = fields.Selection(help="")

    country_id = fields.Many2one(required=True,
        help="""Individuals: Country of Residence
        International Organizations: Country of HQ""")

    community_id = fields.Many2one('sparkit.community', string="Community",
        track_visibility='onchange')

    community_ids = fields.Many2many('sparkit.community', string="Communities",
        track_visibility='onchange')

    new_leader = fields.Selection([('1', 'Yes'), ('0', 'No')],
        select=True, string="New Leader",
        track_visibility='onchange',
        help="Tick this box if the leader has never been in a leadership before.")

    function = fields.Char(string="Job/Leadership Position")
