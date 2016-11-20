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
	phase_id = fields.Many2one(related='community_id.phase_id', string="Phase", store=True,
		readonly=True)
	step_id = fields.Many2one(related='community_id.step_id', string="Step", store=True,
		readonly=True)

	#Capacity
	socialskills = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Social Skills")
	technicalskills = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Project/Technical Skills")
	confidence = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Empowerment: Confidence")
	agency = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Empowerment: Agency")

	#Cohesion
	belonging= fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Sense of Belonging")
	communal_approach = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Communal Approach")
	social_trust= fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Social Trust/Social Capital")
	conflict_resolution = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Conflict(s) Resolution")


	#Leadership
	extent = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Extent")
	quality = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Quality")
	equity_diversity = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Equity/Diversity")
	accountability_transparency = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Accountability/Transparency")

	#Civic Engagement
	commitment = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Commitment")
	participation_quality = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Participation: Quality")
	participation_equity_diversity = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Participation: Equity/Diversity")
	ownership = fields.Selection([(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], select=True,
		string = "Ownership")


	@api.multi
	@api.depends('community_id')
	def _get_name(self):
		for r in self:
			r.name = r.community_id.name + ': ' + str(r.date)
