# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Partnership(models.Model):
	_name = 'sparkit.partnership'

	#Basic
	name = fields.Char(compute='_get_name', readonly=True)
	partner_id = fields.Many2one('res.partner', string="Partner")
	partner_name = fields.Char(related='partner_id.name')
	community_id = fields.Many2one('sparkit.community', string="Community")
	community_number = fields.Char(related='community_id.community_number')
	community_name = fields.Char(related='community_id.name')

	#Partnership Information
	description = fields.Text(string="Partnership Description")
	date = fields.Date(string="Date of Partnership")
	is_active = fields.Boolean(string="Active Partnership?", default=True)

	partnership_update_ids = fields.One2many('sparkit.partnershipupdate', 'partnership_id')

	@api.depends('partner_name', 'community_name', 'community_number')
	def _get_name(self):
		for r in self:
			if r.partner_name and r.community_name and r.community_number:
				r.name = r.community_number + ' ' + r.community_name + ' - ' + r.partner_name


class PartnershipUpdate(models.Model):
	_name = 'sparkit.partnershipupdate'
	_order = 'date desc'

	name = fields.Char(compute='_get_name', readonly=True)
	partnership_id = fields.Many2one('sparkit.partnership', string="Partnership")
	partnership_name = fields.Char(related='partnership_id.name')
	community_id = fields.Many2one('sparkit.community', string="Community")

	date = fields.Date(string="Date")
	description = fields.Text(string="Update")

	@api.depends('partnership_name')
	def _get_name(self):
		for r in self:
			r.name = r.partnership_name + ': ' + str(r.date)
