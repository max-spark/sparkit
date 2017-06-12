# -*- coding: utf-8 -*-

from openerp import models, fields, api

# TODO: Pass number of households at lastest date to SavingsGroup

class SavingsGroup(models.Model):
	_name = 'sparkit.savingsgroup'
	_inherit = 'mail.thread'

	#Basic Fields
	name = fields.Char(compute='_get_name', track_visibility='always')
	community_id = fields.Many2one('sparkit.community', string="Community",
		domain=[('is_partnered', '=', True)], required=True,
		ondelete='cascade', track_visibility='onchange')
	community_number = fields.Char(related='community_id.community_number',
		track_visibility='onchange')
	country_id = fields.Many2one(related='community_id.country_id', readonly=True,
		track_visibility='onchange')

	#Savings Groups
	number_hh_at_start = fields.Integer(
		string="Number of People/Households at Savings Group Start",
		required=True,
		track_visibility='onchange')
	uses_households = fields.Boolean(string="Savings Group Uses Households?",
		help="Please check this box if the savings group uses households to track contributions, instead of people.")
	contribution_frequency = fields.Selection([('weekly', 'Weekly'),
		('biweekly', 'Twice a Month'),
		('monthly', 'Once a Month'),
		('frequently', 'Frequent but irregular collection'),
		('other', 'Other')], select=True, string="Contribution Frequency",
		track_visibility='onchange')
	contribution_amount = fields.Float(string="Minimum Contribution Amount",
		help="Minimum amount per person(or household) at time of collection",
		track_visibility='onchange')
	is_existing = fields.Boolean(string="Did the Savings Group Exist Before Partnership?",
		track_visibility='onchange')
	start_date = fields.Date(string="Date Savings Group Started", required=True,
		track_visibility='onchange')
	end_date = fields.Date(string="Date Savings Group Ended",
		track_visibility='onchange')

	#Calculations
	amount_in_bank = fields.Float(related='latest_id.amount_in_bank', readonly=True,
		track_visibility='onchange')
	amount_in_circulation = fields.Float(related='latest_id.amount_in_circulation', readonly=True,
		track_visibility='onchange')
	number_hh = fields.Integer(related='latest_id.number_hh', readonly=True, default='number_hh_at_start',
		track_visibility='onchange')
	last_updated = fields.Date(compute='_get_latest', readonly=True, string="Last Updated",
		track_visibility='onchange')

	#Calculates the latest ID based on date
	latest_id = fields.Many2one('sparkit.savingsgroupupdate', compute='_get_latest')

	#Total Saved
	total_saved = fields.Float(string="Total Saved", compute='get_total_saved')

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
		for r in self:
			if r.savings_group_update_ids:
				r.latest_id = max(r.savings_group_update_ids.ids)
				if r.latest_id:
					r.last_updated = r.latest_id.date

	@api.multi
	@api.depends('latest_id')
	def get_total_saved(self):
		for r in self:
			if r.latest_id:
				r.total_saved = r.latest_id.amount_in_bank + r.latest_id.amount_in_circulation + r.latest_id.interest_earned

	# Adding followers
	# TODO: Update this once it changes!
	@api.model
	def create(self, vals):
		savings_group = super(SavingsGroup, self).create(vals)
		if savings_group.community_id:
			savings_group.message_subscribe_users(user_ids=[savings_group.community_id.m_e_assistant_id.id, savings_group.community_id.program_manager_id.id, savings_group.community_id.facilitator_id.id])
		return savings_group

class SavingsGroupUpdate(models.Model):
	_name = 'sparkit.savingsgroupupdate'
	_order = 'date desc'

	@api.depends('savings_group_id')
	def _get_default_hh(self):
		for r in self:
			if r.savings_group_id:
				r.number_hh = r.savings_group_id.number_hh

	#Basic
	name = fields.Char(compute='_get_name')
	savings_group_id = fields.Many2one('sparkit.savingsgroup',
		string="Savings Group", ondelete='cascade')
	community_id = fields.Many2one('sparkit.community', ondelete='cascade')

	#Update
	date = fields.Date(string="Date of Update")
	number_hh = fields.Integer(string="Number of Active People/HH",
		help="What is the total number of people/households currently in the savings group?",
		default=_get_default_hh)
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
