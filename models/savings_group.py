# -*- coding: utf-8 -*-

from openerp import models, fields, api

# TODO: Pass number of households at lastest date to SavingsGroup

class SavingsGroup(models.Model):
	_name = 'sparkit.savingsgroup'

	#Basic Fields
	name = fields.Char(compute='_get_name')
	community_id = fields.Many2one('sparkit.community', string="Community",
		domain=[('is_partnered', '=', True)])

	#Savings Groups
	number_hh_at_start = fields.Integer(
		string="Number of Households at Savings Group Start")
	number_women = fields.Integer(string="Number of Women at Savings Group Start")
	number_men = fields.Integer(string="Number of Men at Savings Group Start")
	contribution_frequency = fields.Selection([('weekly', 'Weekly'),
		('biweekly', 'Twice a Month'),
		('monthly', 'Once a Month'),
		('frequently', 'Frequent but irregular collection'),
		('other', 'Other')], select=True, string="Contribution Frequency")
	contribution_amount = fields.Float(string="Contribution Amount",
		help="Amount per person(or household) at time of collection")
	start_capital = fields.Float(string="Amount at Start")
	is_existing = fields.Boolean(string="Did the Savings Group Exist Before Partnership?")
	start_date = fields.Date(string="Date Savings Group Started", required=True)
	end_date = fields.Date(string="Date Savings Group Ended")
	is_sustaining = fields.Boolean(string="Savings Group Sustaining?", default=True)

	#Calculations
	amount_in_bank = fields.Float(related='latest_id.amount_in_bank', readonly=True)
	amount_in_circulation = fields.Float(related='latest_id.amount_in_circulation', readonly=True)
	total_saved = fields.Float(related='latest_id.total_saved', readonly=True)


	#Calculates the latest ID based on date
	latest_id = fields.Many2one('sparkit.savingsgroupupdate', compute='_get_latest')

	#Updates
	savings_group_update_ids = fields.One2many('sparkit.savingsgroupupdate',
		'savings_group_id', string="Updates")

	@api.depends('community_id', 'start_date')
	def _get_name(self):
		for r in self:
			if r.community_id:
				r.name = r.community_id.name + ' - SG ' + str(r.start_date)

	#Function to return the Latest SG Update ID
	@api.multi
	@api.depends('savings_group_update_ids')
	def _get_latest(self):
		if self.savings_group_update_ids:
			latest_date = max(s.date for s in self.savings_group_update_ids)
			latest = self.savings_group_update_ids.search([('date', '=', latest_date), ('savings_group_id.name', '=', self.name)], limit=1)
			if latest:
				self.latest_id = latest


class SavingsGroupUpdate(models.Model):
	_name = 'sparkit.savingsgroupupdate'

	#Basic
	name = fields.Char(compute='_get_name')
	savings_group_id = fields.Many2one('sparkit.savingsgroup',
		string="Savings Group", required=True)
	community_id = fields.Many2one('sparkit.community',
		store=True, readonly=True, string="Community")

	#Update
	date = fields.Date(string="Date of Update")
	number_hh = fields.Integer(string="Number of HH",
		help="What is the total number of households currently in the savings group?")
	total_loans_in_repayment_current = fields.Integer(string="Total Loans in Repayment - Current",
		help="How many loans are currently in repayment?")
	total_loans_in_repayment_all_time = fields.Integer(string="Total Loans in Repayment - All Time",
		help="How many loans has the community loaned out-- and been repaid--in total?")
	total_loans_in_repayment_ontime = fields.Integer(string="Total Loans Repaid on Time - Current",
		help="How many loans that are currently in repayment are being repaid ontime?")
	total_loans_in_repayment_ontime_all_time = fields.Integer(string="Total Loans Repaid on Time - All Time",
		help="How many loans that have been repaid were repaid on time?")
	amount_in_bank = fields.Float(string="Amount in Savings Group Account",
		help="How much has the community saved?")
	amount_in_circulation = fields.Float(string="Amount in Circulation",
		help="Amount of Money Currently Loaned To Members")
	interest_earned = fields.Float(string="Interest Earned",
		help="How much interest has the community earned off loans?")
	total_saved = fields.Float(compute='_get_total_saved',
		help="The total saved is the amount the community has in the bank as well as the amount currently in circulation.")

	@api.depends('savings_group_id', 'date')
	def _get_name(self):
		for r in self:
			if r.savings_group_id:
				r.name = r.savings_group_id.name + ': Update ' + str(r.date)


	@api.depends('amount_in_circulation', 'amount_in_bank')
	def _get_total_saved(self):
		for r in self:
			r.total_saved = r.amount_in_circulation + r.amount_in_bank
