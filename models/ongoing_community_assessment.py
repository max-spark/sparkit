# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime

class OngoingCommunityAssessment(models.Model):
	_name = 'sparkit.oca'

	name = fields.Char(compute='_get_name', string="Form ID")
	country_id = fields.Many2one(related='community_id.country_id', string="Country", readonly=True)
	country_name = fields.Char(compute='_get_country_name', string="Country Name", store=True)
	community_id = fields.Many2one('sparkit.community', string="Community",
		ondelete='cascade')
	date = fields.Date(string="Date of Assessment")
	collected_by = fields.Many2one('res.users', string="Collected By",
		default=lambda self: self.env.user)
	oca_number = fields.Selection(
		[('0', 'Baseline'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('graduated', 'Follow-up with Graduated Community')],
		select=True, string="OCA Number", required=True)
	oca_type = fields.Selection([('long', 'Long'), ('monitoring', 'Monitoring')], select=True, string="OCA Type")

	start_time = fields.Float(string="Start Time")
	end_time = fields.Float(string="End Time")

	#Background
	community_member = fields.Char(string="Community Member", required=True)
	age = fields.Integer(string="Age")
	sex = fields.Selection([(0, 'Male'), (1, 'Female')], select=True,
		string="Sex")
	household_size = fields.Integer(string="Household Size")
	marital_status = fields.Selection([(1, 'Single'), (2, 'Married'), (3, 'Divorced'),
		(4, 'Widowed'), (5, 'Other')], string = "Marital Status")

	#Biggest Concern
	biggestconcern_family = fields.Text(string="What is the biggest concern/most pressing need in your family?")
	biggestconcern_family_category_id = fields.Many2one('sparkit.biggestconcerncategory', string="What is the biggest concern/most pressing need in your family? -category")
	biggestconcern_family_subcategory_id = fields.Many2one('sparkit.biggestconcernsubcategory', string="What is the biggest concern/most pressing need in your family? -specific")
	biggestconcern_cmty= fields.Text(string="What is the biggest concern/most pressing need in your community?")
	biggestconcern_cmty_category_id = fields.Many2one('sparkit.biggestconcerncategory',	string="What is the biggest concern/most pressing need in your community? - category")
	biggestconcern_cmty_subcategory_id = fields.Many2one('sparkit.biggestconcernsubcategory', string="What is the biggest concern/most pressing need in your community? - specific")

	#Section Two: Capacity


	#Section Three: Cohesion

	
	#Section Four: Leadership


	#Section Five: Civic Engagement


	# Cross Sector


	@api.multi
	@api.depends('community_id', 'oca_number', 'community_member')
	def _get_name(self):
		for r in self:
			r.name = r.community_id.name + ' - ' + r.community_member + ': OCA ' + str(r.oca_number)

	@api.depends('country_id')
	def _get_country_name(self):
		for r in self:
			if r.country_id:
				r.country_name = r.country_id.name

	#---------------------------------------------
	#
	#   Biggest Concern categories/subcategories
	#	for OCA questions 12/13
	#
	#---------------------------------------------

class BiggetConcernCategory(models.Model):
	_name = 'sparkit.biggestconcerncategory'

	name = fields.Char(string="Name")
	category_code = fields.Integer(string="Code")
	subcategory_ids = fields.One2many('sparkit.biggestconcernsubcategory', 'category_id',
		string="Sub-Categories")


	_sql_constraints = [
		#Unique Code
		('code_unique',
    	'UNIQUE(category_code)',
    	"The code must be unique"),
    ]

class BiggestConcernSubCategory(models.Model):
	_name = 'sparkit.biggestconcernsubcategory'

	name = fields.Char(string="Name")
	subcategory_code = fields.Integer(string="Code")
	category_id = fields.Many2one('sparkit.biggestconcerncategory',
		string="Biggest Concern Category")


	_sql_constraints = [
		#Unique Code
		('code_unique',
    	'UNIQUE(subcategory_code)',
    	"The code must be unique"),
    ]

class CrossSectorItem(models.Model):
	_name = 'sparkit.crosssectoritem'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")
	filter = fields.Integer(string="Filter: 1-Spark, 0-Baseline")

class CrossSectorAnimal(models.Model):
	_name = 'sparkit.crosssectoranimal'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")
	filter = fields.Integer(string="Filter: 1-Spark: 0-Baseline")

class CrossSectorIllness(models.Model):
	_name = 'sparkit.crosssectorillness'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")
