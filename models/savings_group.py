# -*- coding: utf-8 -*-

from openerp import models, fields, api

# TODO: Pass number of households at lastest date to SavingsGroup

class SavingsGroup(models.Model):
	_name = 'sparkit.savingsgroup'

	#Basic Fields
	name = fields.Char(compute='_get_name')
	community_id = fields.Many2one('sparkit.community', string="Community",
		domain=[('is_partnered', '=', True)], required=True)

	#Savings Groups
	number_hh_at_start = fields.Integer(
		string="Number of Households at Savings Group Start",
		required=True)
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

	#Calculations
	amount_in_bank = fields.Float(related='latest_id.amount_in_bank', readonly=True)
	amount_in_circulation = fields.Float(related='latest_id.amount_in_circulation', readonly=True)
	total_saved = fields.Float(related='latest_id.total_saved', readonly=True)


	#Calculates the latest ID based on date
	latest_id = fields.Many2one('sparkit.savingsgroupupdate', compute='_get_latest')

	#Updates
	savings_group_update_ids = fields.One2many('sparkit.savingsgroupupdate',
		'savings_group_id', string="Updates")

	@api.multi
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
		string="Savings Group")
	community_id = fields.Many2one('sparkit.community')

	#Update
	date = fields.Date(string="Date of Update")
	number_hh = fields.Integer(string="Number of HH",
		help="What is the total number of households currently in the savings group?")
	amount_in_bank = fields.Float(string="Amount in Savings Group Account",
		help="How much has the community saved?", required=True)
	amount_in_circulation = fields.Float(string="Amount in Circulation",
		help="Amount of Money Currently Loaned To Members", required=True)
	interest_earned = fields.Float(string="Interest Earned",
		help="How much interest has the community earned off loans?",
		required=True)
	is_sustaining = fields.Boolean(string="Savings Group Sustaining?", default=True)
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
