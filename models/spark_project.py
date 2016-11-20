# -*- coding: utf-8 -*-

from openerp import models, fields, api

#TODO Potentially add sequences?
#TODO Rename UniqueBudgetItems just to Budget

class SparkProject(models.Model):
	_name = 'sparkit.sparkproject'

	name = fields.Char(compute='_get_project_name')

	#---- Basic Project Information ----#
	community_id = fields.Many2one('sparkit.community', string="Community", required=True,
		domain=[('is_partnered', '=', True)])
	facilitator_id = fields.Many2one('res.users', string="Facilitator")
	community_number = fields.Char(related='community_id.community_number')
	community_name = fields.Char(related='community_id.name')
	category_id = fields.Many2one('sparkit.projectcategory', string="Category")
	subcategory_id = fields.Many2one('sparkit.projectsubcategory', string="Sub-Category")
	grant_agreement_date = fields.Date(string="Grant Agreement Date")
	grant_amount = fields.Float(string="Grant Amount")
	country_id = fields.Many2one(related='community_id.country_id', readonly=True)
	currency_id = fields.Many2one(related='country_id.currency_id', readonly=True, store=True)
	exchange_rate = fields.Float(string="Exchange Rate")
	grant_amount_local = fields.Float(string="Grant Amount - Local Currency",
		compute = '_local_grant_amount', readonly=True)

	#-- Budgeted Contribution Summary --#
	spark_contribution = fields.Float(string="Spark", readonly=True,
		compute='_spark_contribution', store=True)
	spark_contribution_percent = fields.Float(string="Spark Contribution %",
		readonly=True, compute='_spark_contribution_percent', store=True)
	community_contribution = fields.Float(string="Community", readonly=True,
		compute='_community_contribution', store=True)
	community_contribution_percent = fields.Float(string="Community Contribution %",
		readonly=True, compute='_community_contribution_percent', store=True)
	other_contribution = fields.Float(string="Other", readonly=True,
		compute='_other_contribution', store=True)
	other_contribution_percent = fields.Float(string="Other Contribution %",
		readonly=True, compute='_other_contribution_percent', store=True)
	total = fields.Float(string="Total Budget", readonly=True,
		compute='_total', store=True)
	grant_surplus = fields.Float(string="Grant Surplus", readonly=True,
		compute='_grant_surplus', store=True)

	#---- Budget Information ----#
	budget_line_item_ids = fields.One2many('sparkit.projectbudgetitem', 'project_id',
		string="Budget Line Items")

	#--- Transactions ---#
	transaction_ids = fields.One2many('sparkit.transaction', 'project_id',
		string="Transactions")
	total_expenditure = fields.Float(string="Total Expenditure", readonly=True,
		store=True, compute='_get_total_expenditure')
	outstanding_receipts = fields.Float(string="Outstanding Receipts", readonly=True,
		store=True, compute='_get_outstanding_receipts')

	#-- Disbursals --#
	disbursal_ids = fields.One2many('sparkit.disbursal', 'project_id',
		string="Disbursals")
	number_disbursals = fields.Integer(readonly=True, store=True,
		compute='_get_number_disbursals', string="Number of Disbursals")
	total_disbursed = fields.Float(readonly=True, store=True,
		compute='_get_total_disbursed', string="Total Disbursed")
	left_to_disburse = fields.Float(string="Left to Disburse", readonly=True,
		store=True, compute='_get_left_to_disburse')

	#-- Disbursal Requests--#
	disbursal_request_ids = fields.One2many('sparkit.disbursalrequest', 'project_id',
		string="Disbursal Requests")
	number_requests = fields.Integer(string="Number of Disbursal Requests", readonly=True,
		store=True, compute='_get_number_disbursal_requests')

	#-- Project Support Initiatives --#
	project_support_initiative_ids = fields.One2many('sparkit.projectsupportinitiative', 'project_id',
		string="Project Support Initiatives")


	#This function counts the number of disbursal requests made by the community
	@api.multi
	@api.depends('disbursal_request_ids')
	def _get_number_disbursal_requests(self):
		for r in self:
			r.number_requests = len(r.disbursal_request_ids)

	#Uses total expenditure to date (from the transactions object) and
	#total disbursed (from the disbursals object) to calculate the
	#amount in outstanding receipts
	@api.depends('total_expenditure', 'total_disbursed')
	def _get_outstanding_receipts(self):
		for r in self:
			r.outstanding_receipts = r.total_disbursed - r.total_expenditure

	#Counts the total amount of transactions to date made by the community
	@api.multi
	@api.depends('transaction_ids')
	def _get_total_expenditure(self):
		for r in self:
			r.total_expenditure = sum(s.amount for s in r.transaction_ids)

	#Calculates the remaining grant balance (total grant - total disbursed)
	@api.depends('total_disbursed', 'spark_contribution')
	def _get_left_to_disburse(self):
		for r in self:
			r.left_to_disburse = r.spark_contribution - r.total_disbursed

	#Counts the number of disbursals made to the community
	@api.multi
	@api.depends('disbursal_ids')
	def _get_number_disbursals(self):
		for r in self:
			r.number_disbursals = len(r.disbursal_ids)

	#Sums the amount disbursed to the community (in the disbursals object)
	@api.multi
	@api.depends('disbursal_ids')
	def _get_total_disbursed(self):
		for r in self:
			r.total_disbursed = sum(s.amount for s in r.disbursal_ids)

	#Concatenates the community number and name to come up with a project name
	@api.multi
	def _get_project_name(self):
		for r in self:
			if r.community_id:
				r.name = r.community_number + ': ' + r.community_name

	#Calculates the grant surplus (total grant - total budgeted) - relevant
	#for Standardized Grant Communities
	@api.depends('total', 'grant_amount_local')
	def _grant_surplus(self):
		for r in self:
			r.grant_surplus = r.grant_amount_local - r.total

	#Counts the total budgeted
	@api.multi
	@api.depends('budget_line_item_ids')
	def _total(self):
		for r in self:
			r.total = sum(s.budgeted for s in r.budget_line_item_ids)

	#Counts the total amount budgeted for Spark to provide
	@api.multi
	@api.depends('budget_line_item_ids')
	def _spark_contribution(self):
		for r in self:
			r.spark_contribution = sum(s.budgeted for s in r.budget_line_item_ids if s.source == "spark")

	#Counts the total amount budgeted for the Community to provide
	@api.multi
	@api.depends('budget_line_item_ids')
	def _community_contribution(self):
		for r in self:
			r.community_contribution = sum(s.budgeted for s in r.budget_line_item_ids if s.source == "community")

	#Counts the total amount budgeted for another organization/government to provide
	@api.multi
	@api.depends('budget_line_item_ids')
	def _other_contribution(self):
		for r in self:
			r.other_contribution = sum(s.budgeted for s in r.budget_line_item_ids if s.source == "other")

	#Counts the percentage of the total project budget contributed by Spark
	@api.depends('spark_contribution', 'total')
	def _spark_contribution_percent(self):
		for r in self:
			if r.total>0:
				r.spark_contribution_percent = (r.spark_contribution / r.total) * 100

	#Counts the percentage of the total project budget contributed by the community
	@api.depends('community_contribution', 'total')
	def _community_contribution_percent(self):
		for r in self:
			if r.total >0:
				r.community_contribution_percent = (r.community_contribution / r.total) * 100

	#Counts the percentage of the total project budget contributed by another partner
	@api.depends('other_contribution', 'total')
	def _other_contribution_percent(self):
		for r in self:
			if r.total >0:
				r.other_contribution_percent = (r.other_contribution / r.total) * 100

	#Calculates the total grant amount in local currency using Spark's exchange rate
	@api.depends('grant_amount', 'exchange_rate')
	def _local_grant_amount(self):
		for r in self:
			r.grant_amount_local = r.grant_amount * r.exchange_rate


	#---------------------------------------------------------
	#                    Project Budget Items
	#
	# Budget items for the Spark community project
	#	(e.g. vaccines for the cow) to be used in Many2one
	#	list across projects
	#
	# Unique Budget Items is the budget item from the list
	# 	that the community then chooses for their project
	#	which includes the price each community specifically
	#	budgeted for
	#
	#--------------------------------------------------------

class BudgetItems(models.Model):
	_name = 'sparkit.budgetitems'

	name = fields.Char(string="Budget Item Name")
	unit = fields.Char(string="Unit")

class ProjectBudgetItem(models.Model):
	_name = 'sparkit.projectbudgetitem'

	name = fields.Char(related='budget_item_id.name', readonly=True, store=True)
	project_id = fields.Many2one('sparkit.sparkproject')
	community_id = fields.Many2one(related='project_id.community_id', store=True, readonly=True)
	budget_item_id = fields.Many2one('sparkit.budgetitems', string="Budget Item")
	unit = fields.Char(string="Unit", related='budget_item_id.unit',
		readonly=True, store=True)
	unit_cost = fields.Float(string="Unit Cost")
	number_of_units = fields.Float(string="Number of Units")
	source = fields.Selection([('spark', 'Spark'),
		 ('community_cash', 'Community - Cash'),
		 ('community_in_kind', 'Community - In Kind'),
		 ('other', 'Other')], select=True,
		 string="Item Source")
	budgeted = fields.Float(string="Budgeted", compute = '_budgeted_amount',
		readonly=True)
	actual = fields.Float(string="Actual", compute='_actual', readonly=True)
	difference = fields.Float(string="Difference", compute ='_line_item_difference',
		readonly=True)
	budget_phase = fields.Selection([('implementation', 'Implementation'),
		('initial', 'Initial'), ('post_implementation', 'Post Implementation')],
		select=True, string="Budget Phase")

	transaction_ids = fields.One2many('sparkit.transaction', 'budget_item_id',
		string="Transactions")

	@api.multi
	@api.depends('transaction_ids')
	def _actual(self):
		for r in self:
			r.actual = sum(s.amount for s in r.transaction_ids)

	@api.depends('unit_cost', 'number_of_units')
	def _budgeted_amount(self):
		for r in self:
			r.budgeted = r.unit_cost * r.number_of_units

	@api.depends('budgeted', 'actual')
	def _line_item_difference(self):
		for r in self:
			r.difference = r.budgeted - r.actual

	#---------------------------------------------------------
	#                    Transactions
	#
	# Community transactions using budget items
	#
	#---------------------------------------------------------

class Transaction(models.Model):
	_name = 'sparkit.transaction'

	#Meta
	project_id = fields.Many2one('sparkit.sparkproject')
	community_id = fields.Many2one(related='project_id.community_id')

	#Fields
	date = fields.Date(string="Transaction Date")
	budget_item_id = fields.Many2one('sparkit.projectbudgetitem', string="Budget Item")
	amount = fields.Float(string="Amount")
	receipt_number = fields.Integer(string="Receipt Number")
	notes = fields.Text(string="Notes")
	receipt =  fields.Binary(string="Receipt", store=True, attachment=True)


	#---------------------------------------------------------
	#                    Disbursals
	#
	# Disbursal Requests:
	#
	#---------------------------------------------------------

class DisbursalRequest(models.Model):
	_name = 'sparkit.disbursalrequest'

	#meta
	project_id = fields.Many2one('sparkit.sparkproject')
	community_id = fields.Many2one(related='project_id.community_id')
	disbursal_ids = fields.One2many('sparkit.disbursal', 'request_number_id')
	project_name = fields.Char(related='project_id.name')
	name = fields.Char(compute="_compute_name")

	#fields
	disbursal_request_number = fields.Integer(string="Request #")
	date = fields.Date(string="Request Date")
	amount = fields.Float(string="Amount Requested")
	amount_approved = fields.Float(string="Amount Approved")
	disbursed_to_date = fields.Float(readonly=True, store=True, compute='_get_disbursed')
	balance = fields.Float(readonly=True, store=True, compute='_get_balance')


	@api.multi
	@api.depends('disbursal_ids')
	def _get_disbursed(self):
		for r in self:
			r.disbursed_to_date = sum(s.amount for s in r.disbursal_ids)

	@api.multi
	@api.depends('amount_approved', 'disbursed_to_date')
	def _get_balance(self):
		for r in self:
			r.balance = r.amount_approved - r.disbursed_to_date

	@api.multi
	@api.depends('disbursal_request_number')
	def _compute_name(self):
		for r in self:
			r.name = r.project_name + " - Disbursal " + str(r.disbursal_request_number)

class Disbursal(models.Model):
	_name = 'sparkit.disbursal'

	#meta
	project_id = fields.Many2one('sparkit.sparkproject')
	community_id = fields.Many2one(related='project_id.community_id')

	#fields
	date = fields.Date(string="Disbursal Date")
	amount = fields.Float(string="Disbursal Amount")
	note = fields.Text(string="Note")
	given_to_community_by_id = fields.Many2one('res.users', string="Given to Community By")
	cash_given_by_id = fields.Many2one('res.users', string="Cash Given By")
	request_number_id = fields.Many2one('sparkit.disbursalrequest',
		string="Disbursal Requests")
	request_amount = fields.Float(related='request_number_id.disbursed_to_date',
		store=True, readonly=True)
	disbursal_balance = fields.Float(readonly=True, store=True, compute='_get_disbursal_balance')

	@api.multi
	@api.depends('request_number_id', 'request_amount')
	def _get_disbursal_balance(self):
		for r in self:
			r.disbursal_balance = r.request_amount - r.amount

	#---------------------------------------------------------
	#              Project Support Initiatives
	#---------------------------------------------------------

class ProjectSupportInitiative(models.Model):
	_name = 'sparkit.projectsupportinitiative'

	name = fields.Char(compute="_get_name")
	project_id = fields.Many2one('sparkit.sparkproject', string="Project")
	community_id = fields.Many2one('sparkit.community',
		string="Community", store=True, readonly=True)
	project_name = fields.Char(related='project_id.name')

	description = fields.Text(string="Description")
	date = fields.Date(string="Date")

	@api.depends('project_name', 'date')
	def _get_name(self):
		for r in self:
			r.name = r.project_name + " - Support Initiative Update: "  + str(r.date)
