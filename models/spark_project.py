# -*- coding: utf-8 -*-

from openerp import models, fields, api

class SparkProject(models.Model):
	_name = 'sparkit.sparkproject'
	_inherit = 'mail.thread'

	name = fields.Char(compute='_get_project_name', track_visibility='always')

	#---- Basic Project Information ----#
	community_id = fields.Many2one('sparkit.community', string="Community", required=True,
		domain=[('is_partnered', '=', True)], ondelete='cascade', track_visibility='onchange')
	facilitator_id = fields.Many2one('res.users', string="Facilitator", related="community_id.facilitator_id")
	community_number = fields.Char(related='community_id.community_number', track_visibility='onchange')
	community_name = fields.Char(related='community_id.name', track_visibility='onchange')
	category_id = fields.Many2one('sparkit.projectcategory', string="Category", required=True,
		track_visibility='onchange')
	subcategory_id = fields.Many2one('sparkit.projectsubcategory', string="Sub-Category",
		track_visibility='onchange')
	grant_agreement_date = fields.Date(string="Grant Agreement Date",
		track_visibility='onchange')
	grant_amount = fields.Float(string="Grant Amount - USD", track_visibility='onchange',
		compute='_get_usd_grant_amount', readonly=True)
	grant_amount_local = fields.Float(string="Grant Amount - Local Currency",
			track_visibility='onchange')
	country_id = fields.Many2one(related='community_id.country_id', readonly=True,
		track_visibility='onchange')
	currency_id = fields.Many2one(related='country_id.currency_id', readonly=True,
		store=True, track_visibility='onchange')
	exchange_rate = fields.Float(string="Exchange Rate", compute='_get_exchange_rate',
		store=True, track_visibility='onchange')

	#-- Donor Info --#
	donor_funded = fields.Boolean(string="Donor Funded")
	donor_ids = fields.One2many('sparkit.projectdonation', 'project_id',
		string="Project Donors")

	#-- Budgeted Contribution Summary --#
	spark_contribution = fields.Float(string="Spark", readonly=True,
		compute='_spark_contribution', store=True, track_visibility='onchange')
	spark_contribution_percent = fields.Float(string="Spark Contribution %",
		readonly=True, compute='_spark_contribution_percent', store=True,
		track_visibility='onchange')
	inkind_community_contribution = fields.Float(string="In-Kind Community Contribution",
		store=True, compute='_inkind_community_contribution')
	cash_community_contribution = fields.Float(string="Cash Community Contribution",
		store=True, compute='_cash_community_contribution')
	community_contribution = fields.Float(string="Community", readonly=True,
		compute='_community_contribution', store=True, track_visibility='onchange')
	community_contribution_percent = fields.Float(string="Community Contribution %",
		readonly=True, compute='_community_contribution_percent', store=True,
		track_visibility='onchange')
	other_contribution = fields.Float(string="Other", readonly=True,
		compute='_other_contribution', store=True,
		track_visibility='onchange')
	other_contribution_percent = fields.Float(string="Other Contribution %",
		readonly=True, compute='_other_contribution_percent', store=True,
		track_visibility='onchange')
	total = fields.Float(string="Total Budget", readonly=True,
		compute='_total', store=True,
		help="Includes both Spark, community, and other contributions.",
		track_visibility='onchange')
	grant_surplus = fields.Float(string="Grant Surplus", readonly=True,
		compute='_grant_surplus', store=True, track_visibility='onchange',
		help="This field is calculated from the total budgeted items allocated to Spark and the overall grant size.")

	#---- Budget Information ----#
	budget_line_item_ids = fields.One2many('sparkit.projectbudgetitem', 'project_id',
		string="Budget Line Items", track_visibility='onchange')

	#--- Transactions ---#
	transaction_ids = fields.One2many('sparkit.transaction', 'project_id',
		string="Transactions", track_visibility='onchange')
	total_expenditure = fields.Float(string="Total Expenditure", readonly=True,
		store=True, compute='_get_total_expenditure', track_visibility='onchange')
	bank_balance = fields.Float(string="Bank Balance", track_visibility='onchange')
	outstanding_receipts = fields.Float(string="Outstanding Receipts", readonly=True,
		store=True, compute='_get_outstanding_receipts', track_visibility='onchange')
	outstanding_receipts_dollars = fields.Float(string="Outstanding Receipts - $",
		store=True, compute='_get_oustanding_receipt_dollars')

	#-- Disbursals --#
	disbursal_ids = fields.One2many('sparkit.disbursal', 'project_id',
		string="Disbursals", track_visibility='onchange')
	number_disbursals = fields.Integer(readonly=True, store=True,
		compute='_get_number_disbursals', string="Number of Disbursals",
		track_visibility='onchange')
	total_disbursed = fields.Float(readonly=True, store=True,
		compute='_get_total_disbursed', string="Total Disbursed",
		track_visibility='onchange')
	left_to_disburse = fields.Float(string="Left to Disburse", readonly=True,
		store=True, compute='_get_left_to_disburse', track_visibility='onchange')
	last_disbursal_date = fields.Date(string="Last Disbursement",
		compute='get_last_disbursement', track_visibility='onchange')

	#-- Disbursal Requests--#
	disbursal_request_ids = fields.One2many('sparkit.disbursalrequest', 'project_id',
		string="Disbursal Requests", track_visibility='onchange')
	number_requests = fields.Integer(string="Number of Disbursal Requests", readonly=True,
		store=True, compute='_get_number_disbursal_requests', track_visibility='onchange')

	#-- Project Support Initiatives --#
	project_support_initiative_ids = fields.One2many('sparkit.projectsupportinitiative', 'project_id',
		string="Project Support Initiatives", track_visibility='onchange')


	#This function counts the number of disbursal requests made by the community
	@api.multi
	@api.depends('disbursal_request_ids')
	def _get_number_disbursal_requests(self):
		for r in self:
			r.number_requests = len(r.disbursal_request_ids)


	# Calculates exchange rate when budget is formed
	@api.multi
	@api.depends('currency_id')
	def _get_exchange_rate(self):
		for r in self:
			if r.currency_id:
				r.exchange_rate = r.currency_id.rate

	@api.multi
	@api.depends('disbursal_ids')
	def get_last_disbursement(self):
		for r in self:
			if r.disbursal_ids:
				r.last_disbursal_date = max(line.date for line in r.disbursal_ids)

	#Uses total expenditure to date (from the transactions object) and
	#total disbursed (from the disbursals object) to calculate the
	#amount in outstanding receipts
	@api.depends('total_expenditure', 'total_disbursed', 'bank_balance')
	def _get_outstanding_receipts(self):
		for r in self:
			r.outstanding_receipts = r.total_disbursed - r.bank_balance - r.total_expenditure

	@api.depends('outstanding_receipts', 'grant_amount')
	def _get_oustanding_receipt_dollars(self):
		for r in self:
			if r.outstanding_receipts and r.exchange_rate:
				r.outstanding_receipts_dollars = r.outstanding_receipts / r.exchange_rate

	#Counts the total amount spent by communities if the budget source is equal to Spark
	@api.multi
	@api.depends('transaction_ids', 'budget_line_item_ids')
	def _get_total_expenditure(self):
		for r in self:
			r.total_expenditure = sum(s.actual for s in r.budget_line_item_ids if s.source == "spark")


	#Calculates the remaining grant balance (total grant - total disbursed)
	@api.depends('total_disbursed', 'grant_amount_local')
	def _get_left_to_disburse(self):
		for r in self:
			r.left_to_disburse = r.grant_amount_local - r.total_disbursed

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
	@api.depends('community_id', 'category_id')
	def _get_project_name(self):
		for r in self:
			if r.community_id and r.category_id:
				r.name = r.country_id.name + ': ' + r.community_number + ': ' + r.community_name + ': ' + r.category_id.name

	#Calculates the grant surplus (total grant - total budgeted) - relevant
	#for Standardized Grant Communities
	@api.depends('total', 'grant_amount_local')
	def _grant_surplus(self):
		for r in self:
			r.grant_surplus = r.grant_amount_local - r.spark_contribution

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

	@api.multi
	@api.depends('budget_line_item_ids')
	def _inkind_community_contribution(self):
		for r in self:
			r.inkind_community_contribution = sum(s.budgeted for s in r.budget_line_item_ids if s.source == "community_in_kind")

	@api.multi
	@api.depends('budget_line_item_ids')
	def _cash_community_contribution(self):
		for r in self:
			r.cash_community_contribution = sum(s.budgeted for s in r.budget_line_item_ids if s.source == "community_cash")

	#Counts the total amount budgeted for the Community to provide, including both inkind and cash
	@api.multi
	@api.depends('inkind_community_contribution', 'cash_community_contribution')
	def _community_contribution(self):
		for r in self:
			r.community_contribution = r.inkind_community_contribution + r.cash_community_contribution

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
	@api.depends('grant_amount_local', 'exchange_rate')
	def _get_usd_grant_amount(self):
		for r in self:
			if r.exchange_rate>0:
				r.grant_amount = r.grant_amount_local / r.exchange_rate




	#---------------------------------------------------------
	#                    Project Budget Items
	#
	# Budget items for the Spark community project
	#	(e.g. vaccines for the cow) to be used in Many2one
	#	list across projects
	#
	# Project Budget Items is the budget line item from the list
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
	_inherit = 'mail.thread'

	name = fields.Char(compute='get_name', readonly=True,
		store=True)
	project_id = fields.Many2one('sparkit.sparkproject', ondelete='cascade',
		track_visibility='onchange')
	community_id = fields.Many2one(related='project_id.community_id', store=True,
		readonly=True, ondelete='cascade', track_visibility='onchange')
	budget_item_id = fields.Many2one('sparkit.budgetitems', string="Budget Item",
		track_visibility='onchange')
	unit = fields.Char(string="Unit", related='budget_item_id.unit',
		readonly=True, store=True, track_visibility='onchange')
	unit_cost = fields.Float(string="Unit Cost", track_visibility='onchange')
	number_of_units = fields.Float(string="Number of Units", track_visibility='onchange')
	source = fields.Selection([('spark', 'Spark'),
		 ('community_cash', 'Community - Cash'),
		 ('community_in_kind', 'Community - In Kind'),
		 ('other', 'Other')], select=True,
		 string="Item Source", track_visibility='onchange')
	budgeted = fields.Float(string="Budgeted", compute = '_budgeted_amount',
		readonly=True, track_visibility='onchange')
	actual = fields.Float(string="Actual", compute='_actual', readonly=True,
		track_visibility='onchange')
	difference = fields.Float(string="Difference", compute ='_line_item_difference',
		readonly=True, track_visibility='onchange')
	implementation_month = fields.Selection([
		('1', 'Implementation Month 1'),
		('2', 'Implementation Month 2'),
		('3', 'Implementation Month 3'),
		('4', 'Implementation Month 4'),
		('5', 'Implementation Month 5'),
		('6', 'Implementation Month 6'),
		('other', 'Other'),], select=True, string="Implementation Month",
		track_visibility='onchange')
	proportion_spent = fields.Float(string="% Spent", compute='_get_proportion_spent')

	# Linking budget items to receipts (Transations)
	transaction_ids = fields.One2many('sparkit.transaction', 'budget_item_id',
		string="Transactions", track_visibility='onchange')

	@api.multi
	@api.depends('transaction_ids')
	def _actual(self):
		for r in self:
			r.actual = sum(s.amount for s in r.transaction_ids)

	@api.multi
	@api.depends('actual', 'budgeted')
	def _get_proportion_spent(self):
		for r in self:
			if r.budgeted > 0:
				r.proportion_spent = (r.actual / r.budgeted) * 100

	@api.depends('unit_cost', 'number_of_units')
	def _budgeted_amount(self):
		for r in self:
			r.budgeted = r.unit_cost * r.number_of_units

	@api.depends('budgeted', 'actual')
	def _line_item_difference(self):
		for r in self:
			r.difference = r.budgeted - r.actual

	@api.depends('project_id', 'budget_item_id', "implementation_month")
	def get_name(self):
		for r in self:
			if r.project_id and r.budget_item_id:
				if r.implementation_month:
					r.name = r.budget_item_id.name + ": Month " + r.implementation_month
				else:
					r.name = r.budget_item_id.name

	#---------------------------------------------------------
	#                    Transactions
	#
	# Community transactions using budget items
	#
	#---------------------------------------------------------

class Transaction(models.Model):
	_name = 'sparkit.transaction'
	_inherit = 'mail.thread'

	#Meta
	project_id = fields.Many2one('sparkit.sparkproject', ondelete='cascade',
		track_visibility='always')
	community_id = fields.Many2one(related='project_id.community_id',
		ondelete='cascade', track_visibility='onchange')

	#Fields
	date = fields.Date(string="Transaction Date", track_visibility='onchange')
	budget_item_id = fields.Many2one('sparkit.projectbudgetitem',
		string="Budget Item", track_visibility='onchange')
	amount = fields.Float(string="Amount", track_visibility='onchange')
	receipt_number = fields.Char(string="Receipt Number", track_visibility='onchange')
	receipt_filename = fields.Char(string="Receipt Filename")
	notes = fields.Text(string="Notes", track_visibility='onchange')
	receipt =  fields.Binary(string="Receipt", store=True, attachment=True,
		track_visibility='onchange')

	# Spark receipt?
	spark_receipt = fields.Boolean(string="Vendor Receipt?",
		help="Check this box if the receipt the community provided was a vendor receipt and NOT a Spark receipt.")


	#---------------------------------------------------------
	#                    Disbursals
	#
	# Disbursal Requests:
	#
	#---------------------------------------------------------

class DisbursalRequest(models.Model):
	_name = 'sparkit.disbursalrequest'
	_inherit = 'mail.thread'

	#meta
	project_id = fields.Many2one('sparkit.sparkproject', ondelete='cascade',
		track_visibility='always')
	community_id = fields.Many2one(related='project_id.community_id',
		ondelete='cascade', track_visibility='onchange')
	disbursal_ids = fields.One2many('sparkit.disbursal', 'request_number_id',
		track_visibility='onchange')
	project_name = fields.Char(related='project_id.name', track_visibility='onchange')
	name = fields.Char(compute="_compute_name", track_visibility='onchange')

	#fields
	disbursal_request_number = fields.Integer(string="Request #",
		track_visibility='onchange')
	date = fields.Date(string="Request Date", track_visibility='onchange')
	amount = fields.Float(string="Amount Requested", track_visibility='onchange')
	amount_approved = fields.Float(string="Amount Approved", track_visibility='onchange')
	disbursed_to_date = fields.Float(readonly=True, store=True, compute='_get_disbursed',
		track_visibility='onchange')
	balance = fields.Float(readonly=True, store=True, compute='_get_balance',
		track_visibility='onchange')
	disbursal_request_hard_copy = fields.Binary(string="Disbursal Request Hard Copy", store=True,
		attachment=True, track_visibility='onchange')
	disbursal_request_hard_copy_name = fields.Char(string="Disbursal Request Hard Copy Name")

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
			if r.project_name and r.disbursal_request_number:
				r.name = r.project_name + " - Disbursal " + str(r.disbursal_request_number)

class Disbursal(models.Model):
	_name = 'sparkit.disbursal'
	_inherit = 'mail.thread'

	#meta
	project_id = fields.Many2one('sparkit.sparkproject', ondelete='cascade',
		track_visibility='always')
	community_id = fields.Many2one(related='project_id.community_id', ondelete='cascade')

	#fields
	date = fields.Date(string="Disbursal Date", track_visibility='onchange')
	amount = fields.Float(string="Disbursal Amount", track_visibility='onchange')
	note = fields.Text(string="Note", track_visibility='onchange')
	payment_method = fields.Selection([('cash', 'Cash'), ('wire_transfer', 'Wire Transfer'),
		('check', 'Check')], select=True, string="Payment Method",
		track_visibility='onchange')
	deposited_in_bank_by = fields.Many2one('res.users', string="Deposited/Cash Given By",
		track_visibility='onchange')
	request_number_id = fields.Many2one('sparkit.disbursalrequest',
		string="Disbursal Requests", track_visibility='onchange')
	request_amount = fields.Float(related='request_number_id.disbursed_to_date',
		store=True, readonly=True, track_visibility='onchange')
	disbursal_balance = fields.Float(readonly=True, store=True, compute='_get_disbursal_balance',
		track_visibility='onchange')
	disbursal_receipt = fields.Binary(string="Disbursal Receipt", store=True,
		attachment=True, track_visibility='onchange')
	disbursal_receipt_name = fields.Char(string="Disbursal Receipt Name")

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
	_inherit = 'mail.thread'

	name = fields.Char(compute="_get_name")
	project_id = fields.Many2one('sparkit.sparkproject', string="Project",
		ondelete='cascade', track_visibility='onchange')
	community_id = fields.Many2one('sparkit.community', ondelete='cascade',
		string="Community", store=True, readonly=True, track_visibility='onchange')
	project_name = fields.Char(related='project_id.name', track_visibility='onchange')

	description = fields.Text(string="Description", track_visibility='onchange')
	date = fields.Date(string="Date", track_visibility='onchange')

	@api.depends('project_name', 'date')
	def _get_name(self):
		for r in self:
			r.name = r.project_name + " - Support Initiative Update: "  + str(r.date)

	#---------------------------------------------------------
	#             Donor Funded Projects Module
	#---------------------------------------------------------

class ProjectDonation(models.Model):
	_name = 'sparkit.projectdonation'

	name = fields.Char(compute="_get_name")
	donor_id = fields.Many2one('res.partner', string="Donor(s)",
		domain=[('company_type', '=', 'donor')])
	amount = fields.Float(string="Amount Committed (USD)")
	donation_date = fields.Date(string="Date of Donation")
	project_id = fields.Many2one('sparkit.sparkproject', string="Project")

	@api.depends('project_id', 'donor_id')
	def _get_name(self):
		for r in self:
			r.name = r.project_id.name + ": " + r.donor_id.name
