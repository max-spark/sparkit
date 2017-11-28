# -*- coding: utf-8 -*-

from openerp import models, fields, api

# Independent Projects module including parent object (the project) and
# a child object (update forms) to allow staff to routinely update
# progress on community independent projects.

class IndependentProject(models.Model):
	_name = 'sparkit.independentproject'
	_inherit = 'mail.thread'

	#Basic Fields
	name = fields.Char(compute='_get_name', track_visibility='always')
	number_project_updates = fields.Integer(default=0, compute='_get_number',
		track_visibility='onchange')
	community_id = fields.Many2one('sparkit.community', string="Community",
		ondelete='cascade', domain=[('is_partnered', '=', True)],
		required=True,
		track_visibility='onchange')
	community_name = fields.Char(related='community_id.name',
		track_visibility='onchange')

	#Category
	project_category_id = fields.Many2one('sparkit.projectcategory', required=True,
		string="Project Category",
		track_visibility='onchange')
	project_subcategory_id = fields.Many2one('sparkit.projectsubcategory',
		required=True, string="Project SubCategory",
		track_visibility='onchange')

	#Project Dates
	start_date = fields.Date(string="Date Independent Project Started",
		track_visibility='onchange')
	end_date = fields.Date(string="Date Independent Project Ended",
		track_visibility='onchange')

	# Project description
	description = fields.Text(string="Description of Independent Project",
		track_visibility='onchange')

	#Updates
	project_update_ids = fields.One2many('sparkit.independentprojectupdate',
		'independent_project_id', string="Updates", ondelete='cascade')

	# Creating Project Name
	@api.multi
	def _get_name(self):
		for r in self:
			if r.community_id and r.project_subcategory_id:
				if r.start_date:
					r.name = r.community_id.name + ' - ' + r.project_subcategory_id.name + ' - ' + r.start_date
				else:
					r.name = r.community_id.name + ' - ' + r.project_subcategory_id.name + ' - Pre-2017'

	# Calculates Number of Update Forms for the Independent Project
	@api.multi
	@api.depends('project_update_ids')
	def _get_number(self):
		for r in self:
			if r.project_update_ids:
				r.number_project_updates = len(r.project_update_ids)

	# Adding followers
	# TODO: Update this once it changes!
	@api.model
	def create(self, vals):
		ind_project = super(IndependentProject, self).create(vals)
		if ind_project.community_id:
			ind_project.message_subscribe_users(user_ids=[ind_project.community_id.m_e_assistant_id.id, ind_project.community_id.program_manager_id.id, ind_project.community_id.facilitator_id.id])
		return ind_project

class IndependentProjectUpdate(models.Model):
	_name = 'sparkit.independentprojectupdate'
	_order = 'date desc'

	#Basic
	name = fields.Char(string="Name")
	independent_project_id = fields.Many2one('sparkit.independentproject',
		string="Independent Project", ondelete='cascade')
	community_id = fields.Many2one('sparkit.community', ondelete='cascade')
	is_sustaining = fields.Boolean(string="Independent Project Sustaining?", default=True)

	#Update
	date = fields.Date(string="Date of Update", required=True)
	update = fields.Text(string="Project Update")
	update_description = fields.Text(string="Update Description", required=True)

	@api.depends('independent_project_name', 'date')
	def _get_name(self):
		for r in self:
			if r.independent_project_id:
				r.name = r.independent_project_id.name + ' ' + str(r.date)
