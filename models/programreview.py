# -*- coding: utf-8 -*-

# These two objects track community advocacy (partnerships).

# The parent object - 'sparkit.partnership' - creates a new
# advocacy record for the community.

# The child object - sparkit.partnershipupdate' - creates updates
# for the parent object.

from openerp import models, fields, api

class ProgramReview(models.Model):
	_name = 'sparkit.programreview'
	_order = 'quarter desc'

	name = fields.Char(compute='_get_name', readonly=True)
	community_id = fields.Many2one('sparkit.community',
		string="Community", ondelete='cascade')
	community_name = fields.Char(related='community_id.name')
	quarter = fields.Selection([('1', 'Q1 2017'),
		('2', 'Q2 2017'),
		('3', 'Q3 2017'),
		('4', 'Q4 2017'),
		('5', 'Q1 2018'),
		('6', 'Q2 2018'),
		('7', 'Q3 2018'),
		('8', 'Q4 2018')], select=True, string="Quarter")
	color = fields.Selection([('green', 'Green'),
		('yellow', 'Yellow'),
		('red', 'Red')], select=True, string="Color")
	quarter_review = fields.Text(string="Quarter Review")
	comments = fields.Text(string="Comments")
	quarter_name = fields.Char(compute='_get_quarter_name', string="Quarter Name", store=True)
	country = fields.Char(compute='_get_country', readonly=True)
	country_region = fields.Char(compute='_get_region', readonly=True)

	@api.one
	@api.depends('quarter')
	def _get_quarter_name(self):
		for r in self:
			if r.quarter:
				r.quarter_name = dict(self.fields_get(allfields=['quarter'])['quarter']['selection'])[self.quarter]

	@api.multi
	def _get_name(self):
		for r in self:
			if r.community_id and r.quarter_name:
				r.name = r.community_id.community_number + ' ' + r.community_id.name + ' - ' + r.quarter_name

	@api.depends('community_id')
	def _get_country(self):
		for r in self:
			if r.community_id:
				r.country = r.community_id.country_id.name

	@api.depends('community_id')
	def _get_region(self):
		for r in self:
			if r.community_id:
				r.country_region = r.community_id.country_region