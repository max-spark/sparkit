# -*- coding: utf-8 -*-

from openerp import models, fields, api

#FCAP Map includes FCAP phases, steps, activity categories and activities

class FCAPMap(models.Model):
	_name = 'sparkit.fcapmap'

	name = fields.Char(string="Name")
	phase = fields.Selection([('planning', 'Planning'),
		('implementation', 'Implementation'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated'),
		('community_identification', 'Community Identification'),
		('partnership_ended', 'Partnership Ended')], select=True, string="Phase")
	step_ids = fields.One2many('sparkit.fcapstep', 'phase_id', String="Steps")
	category_ids = fields.One2many('sparkit.fcapcategory', 'phase_id', string="Categories")
	activity_ids = fields.One2many('sparkit.fcapactivity', 'phase_id', string="Activities")

class FCAPStep(models.Model):
	_name = 'sparkit.fcapstep'
	_order = 'step_number'

	name = fields.Char("FCAP Step")
	phase_id = fields.Many2one('sparkit.fcapmap', string="Phase ID")
	phase = fields.Selection(related='phase_id.phase', string="Phase")
	step_number = fields.Integer(string="Step Number")
	duration = fields.Integer(string="Duration")

class FCAPCategory(models.Model):
	_name = 'sparkit.fcapcategory'

	name = fields.Char(string="Category")
	phase_id = fields.Many2one('sparkit.fcapmap', string="Phase ID")
	phase = fields.Selection(related='phase_id.phase', string="Phase")

class FCAPActivity(models.Model):
	_name = 'sparkit.fcapactivity'

	name = fields.Char(string="Activity")
	category_id = fields.Many2one('sparkit.fcapcategory', string="Category", required=True)
	phase_id = fields.Many2one('sparkit.fcapmap', string="Phase ID")
	phase = fields.Selection(related='phase_id.phase', string="Phase")
