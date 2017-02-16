# -*- coding: utf-8 -*-

from openerp import models, fields, api

#Independent Projects

class IndependentProject(models.Model):
	_name = 'sparkit.independentproject'

	#Basic Fields
	name = fields.Char(compute='_get_name')
	number_project_updates = fields.Integer(default=0, compute='_get_number')
	community_id = fields.Many2one('sparkit.community', string="Community",
		ondelete='cascade', domain=[('is_partnered', '=', True)],
		required=True)
	community_name = fields.Char(related='community_id.name')

	#Category
	project_category_id = fields.Many2one('sparkit.projectcategory', required=True,
		string="Project Category")
	project_subcategory_id = fields.Many2one('sparkit.projectsubcategory',
		required=True, string="Project SubCategory")

	#Project Dates
	start_date = fields.Date(string="Date Independent Project Started")
	end_date = fields.Date(string="Date Independent Project Ended")

	#Updates
	project_update_ids = fields.One2many('sparkit.independentprojectupdate',
		'independent_project_id', string="Updates", ondelete='cascade')

	# Creating Project Name
	@api.multi
	def _get_name(self):
		for r in self:
			if r.community_id and r.project_subcategory_id:
				r.name = 'IND: ' + r.community_id.name + ' - ' + r.project_subcategory_id.name

	# Calculates Number of Update Forms for the Independent Project
	@api.multi
	@api.depends('project_update_ids')
	def _get_number(self):
		for r in self:
			if r.project_update_ids:
				r.number_project_updates = len(r.project_update_ids)


class IndependentProjectUpdate(models.Model):
	_name = 'sparkit.independentprojectupdate'
	_order = 'date desc'

	#Basic
	name = fields.Char(string="Name")
	independent_project_id = fields.Many2one('sparkit.independentproject',
		string="Independent Project", ondelete='cascade')
	community_id = fields.Many2one('sparkit.community')
	is_sustaining = fields.Boolean(string="Independent Project Sustaining?", default=True)

	#Update
	date = fields.Date(string="Date of Update", required=True)
	update = fields.Text(string="Project Update", required=True)

	@api.depends('independent_project_name', 'date')
	def _get_name(self):
		for r in self:
			if r.independent_project_id:
				r.name = r.independent_project_id.name + ' ' + str(r.date)
