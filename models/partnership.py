# -*- coding: utf-8 -*-

# These two objects track community advocacy (partnerships).

# The parent object - 'sparkit.partnership' - creates a new
# advocacy record for the community.

# The child object - sparkit.partnershipupdate' - creates updates
# for the parent object.

from openerp import models, fields, api

class Partnership(models.Model):
	_name = 'sparkit.partnership'
	_inherit = 'mail.thread'

	#Basic
	name = fields.Char(compute='_get_name', readonly=True, track_visibility='always')
	partner_id = fields.Many2one('res.partner', string="Partner", required=True,
		domain="[('company_type', '=', 'company')]",
		track_visibility='onchange')
	community_id = fields.Many2one('sparkit.community', string="Community",
		required=True, ondelete='cascade',
		track_visibility='onchange')

	#Partnership Information
	description = fields.Text(string="Partnership Description",
		required=True, track_visibility='onchange')
	date_reached_out = fields.Date(string="Date Community Reached Out To Partner",
		help="When did the community reach out to the partner?",
		required=True, track_visibility='onchange')
	start_date = fields.Date(string="Start Date of Partnership",
		track_visibility='onchange',
		help="When was the partnership agreement between the community and partner signed? When did the partnership start?")
	end_date = fields.Date(string="End Date of Partnership",
		track_visibility='onchange',
		help="What date did the partnership end?")
	is_active = fields.Boolean(string="Active Partnership?", default=True, track_visibility='onchange')
	succesful_partnership = fields.Boolean(string="Succesful Advocacy Attempt", track_visibility='onchange')

	# Memorandum of Understanding - Upload field
	mou_name = fields.Char(string="M.O.U. File Name",
		compute='_get_mou_name', track_visibility='onchange')
	mou = fields.Binary(string="Memorandum of Understanding",
		help="Upload a PDF of the Memorandum of Understanding")

	partnership_update_ids = fields.One2many('sparkit.partnershipupdate', 'partnership_id')

	@api.depends('name')
	def _get_mou_name(self):
		for r in self:
				if r.name:
					r.mou_name = r.name + '_' + 'Memorandum_of_Understanding'

	@api.multi
	def _get_name(self):
		for r in self:
			if r.partner_id and r.community_id:
				r.name = r.community_id.community_number + ' ' + r.community_id.name + ' - ' + r.partner_id.name

	# Adding followers
	# TODO: Update this once it changes!
	@api.model
	def create(self, vals):
		partnership = super(Partnership, self).create(vals)
		if partnership.community_id:
			partnership.message_subscribe_users(user_ids=[partnership.community_id.m_e_assistant_id.id, partnership.community_id.program_manager_id.id, partnership.community_id.facilitator_id.id])
		return partnership


class PartnershipUpdate(models.Model):
	_name = 'sparkit.partnershipupdate'
	_order = 'date desc'

	name = fields.Char(compute='_get_name', readonly=True)
	partnership_id = fields.Many2one('sparkit.partnership',
		string="Partnership", ondelete='cascade')
	partnership_name = fields.Char(related='partnership_id.name')
	level_of_support = fields.Selection([('1', 'Strongly Opposed'),
		('2', 'Opposed'),
		('3', 'Indifferent'),
		('4', 'Supports'),
		('5', 'Strongly Supports')], select=True, string="Level of Support")
	community_id = fields.Many2one('sparkit.community', string="Community",
		ondelete='cascade')

	date = fields.Date(string="Date")

	description = fields.Text(string="Update")

	@api.depends('partnership_name')
	def _get_name(self):
		for r in self:
			if r.partnership_name and r.date:
				r.name = r.partnership_name + ': ' + str(r.date)
