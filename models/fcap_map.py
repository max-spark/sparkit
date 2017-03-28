# -*- coding: utf-8 -*-

from openerp import models, fields, api

#FCAP Map includes FCAP phases, steps, activity categories and activities

class FCAPMap(models.Model):
	_name = 'sparkit.fcapmap'

	# Default FCAP Phases. These phases are the broader bucket categories that
	# each state (in Spark terms, step) fall into. Then, each state(step)
	# has certain activities that facilitators use in meetings.
	name = fields.Char(string="Phase")
	phase = fields.Selection([('planning', 'Planning'),
		('implementation', 'Implementation'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated'),
		('community_identification', 'Community Identification'),
		('partnership_ended', 'Partnership Ended')], select=True,
		string="Phase")
	step_ids = fields.One2many('sparkit.fcapstep', 'phase_id', string="Steps")

class FCAPStep(models.Model):
	_name = 'sparkit.fcapstep'

	name = fields.Char(string="Name")
	phase_id = fields.Many2one('sparkit.fcapmap', string="Phase",
		ondelete='cascade')
	state = fields.Selection([
		('community_identification', 'Community Identification - Baseline'),
		('introductions', 'Introductions'),
		('partnership', 'Partnership'),
		('community_building', 'Community Building'),
		('goal_setting_goals', 'Goal Setting: Goals'),
		('goal_setting_pathways', 'Goal Setting: Pathways'),
		('implementation_plan', 'Proposal Development: Implementation Plan'),
		('operational_plan', 'Proposal Development: Operational Plan'),
		('measuring_success', 'Proposal Development: Measuring Success'),
		('sustainability_plan', 'Proposal Development: Sustainability Plan'),
		('proposal_review', 'Proposal Development: Proposal Finalization'),
		('grant_agreement', 'Implementation: Grant Agreement & Financial Management'),
		('first_disbursement', 'Implementation: First Disbursement, Accountability & Transparency'),
		('leadership', 'Implementation: Leadership'),
		('transition_strategy', 'Implementation: Transition Strategy'),
		('post_implementation', 'Post Implementation'),
		('post_implementation1', 'Post Implementation: Management Support'),
		('post_implementation2', 'Post Implementation: Future Envisioning'),
		('post_implementation3', 'Post Implementation: Graduation Preparation'),
		('graduated', 'Graduated'),
		('partnership_canacelled', 'Partnership Cancelled')],
		string="Step")
	min_duration = fields.Integer(string="Minimum Duration")
	step_number = fields.Integer(string="Step Number")
	activity_ids = fields.One2many('sparkit.fcapactivity', 'step_id', string="Activities")

class FCAPActivity(models.Model):
	_name = 'sparkit.fcapactivity'

	name = fields.Char(string="Name")
	step_id = fields.Many2one('sparkit.fcapstep', string="Step")
	# Number to be able to search record (other than by name) in community.py
	# for FCAP workflow
	number = fields.Integer(string="Number")
