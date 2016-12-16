# -*- coding: utf-8 -*-

from openerp import models, fields, api

#Pillar Assessment form

class PillarAssessment(models.Model):
	_name = 'sparkit.pillarassessment'

	#Information
	name = fields.Char(compute='_get_name')
	country_id = fields.Many2one(related='community_id.country_id', string="Country",
		readonly=True)
	community_id = fields.Many2one('sparkit.community', string="Community", required=True)
	collected_by_id = fields.Many2one('res.users', string="Collected By", required=True,
		default=lambda self: self.env.user)
	entered_by_id = fields.Many2one('res.users', string="Entered By", required=True,
		default=lambda self: self.env.user)
	date = fields.Date(string="Date Collected")
	phase = fields.Char(compute='_get_phase', store=True,
		readonly=True, string="Phase")
	state = fields.Char(compute='_get_step', store=True,
		readonly=True, string="Step")


	#Capacity
	socialskills = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Social Skills", required=True)
	technicalskills = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Project/Technical Skills", required=True)
	confidence = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Empowerment: Confidence", required=True)
	agency = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Empowerment: Agency", required=True)

	#Cohesion
	belonging= fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Sense of Belonging", required=True)
	communal_approach = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Communal Approach", required=True)
	social_trust= fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Social Trust/Social Capital", required=True)
	conflict_resolution = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Conflict(s) Resolution", required=True)


	#Leadership
	extent = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Extent", required=True)
	quality = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Quality", required=True)
	equity_diversity = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Equity/Diversity", required=True)
	accountability_transparency = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Accountability/Transparency", required=True)

	#Civic Engagement
	commitment = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Commitment", required=True)
	participation_quality = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Participation: Quality", required=True)
	participation_equity_diversity = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Participation: Equity/Diversity", required=True)
	ownership = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Ownership", required=True)

	@api.multi
	@api.depends('community_id')
	def _get_name(self):
		for r in self:
			r.name = r.community_id.name + ': ' + str(r.date)

	@api.depends('community_id')
	def _get_phase(self):
		for r in self:
			if r.community_id.phase:
				r.phase = r.community_id.phase_name

	@api.multi
	@api.depends('community_id')
	def _get_step(self):
		for r in self:
			if r.community_id.state:
				r.state = r.community_id.state_name
