# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ScoutingForm(models.Model):
	_name = 'sparkit.scoutingform'

	#Basic Information
	name = fields.Char(string="Name")
	community_id = fields.Many2one('sparkit.community', string="Community")
	country_id = fields.Many2one(related='community_id.country_id', string="Country")
	scouting_date = fields.Date(string="Scouting Date")
	group_type = fields.Selection([('village', 'Village'), ('association', 'Association'),
		('cooperative', 'Cooperative'), ('other', 'Other')], select=True,
		string="Group Type")
	facilitator_id = fields.Many2one('res.users', default=lambda self: self.env.user,
		string="Facilitator")
	attendance = fields.Integer(string="Scouting - Attendance")
	num_of_households = fields.Integer(string="Scouting - Number of Households")
	gps_coordinates = fields.Char(string="Community GPS Coordinates")
	how_cmty_was_identified = fields.Text(string="How was the community identified?")

	#Location
	district = fields.Char(string="District")
	sector = fields.Char(string="Sector")
	village = fields.Char(string="Village")
	cell = fields.Char(string="Cell")
	province = fields.Char(string="Province")
	sub_county = fields.Char(string="Sub-County")
	city = fields.Char(string="City")

	#Primary Contacts
	primary_contact_ids = fields.Many2many('res.partner', string="Primary Contacts")

	#Pillar Rankings
	civicengagement_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Civic Engagement: Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	civicengagement_desc = fields.Text(string="Civic Engagement: Description",
		help="Please briefly describe the reason for your ranking.")
	cohesion_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Cohesion: Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	cohesion_desc = fields.Text(string="Cohesion: Description",
		help="Please briefly describe the reason for your ranking.")
	leadership_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Leadership: Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	leadership_desc = fields.Text(string="Leadership: Description",
		help="Please briefly describe the reason for your ranking.")
	capacity_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Capacity: Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	capacity_desc = fields.Text(string="Capacity: Description",
		help="Please briefly describe the reason for your ranking.")
	sustainable_project_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Sustainable Project: Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	sustainable_project_desc = fields.Text(string="Sustainable Project: Description",
		help="Please briefly describe the reason for your ranking.")
	vulnerability_project_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Vulnerability: Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	vulnerability_project_desc = fields.Text(string="Vulnerability: Description",
		help="Please briefly describe the reason for your ranking.")

	#Recommendation
	overall_ranking = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
		('4', '4'), ('5', '5')], select=True, string="Overall Ranking",
		help="Please rate the community's level, with 1 as the lowest and 5 as the highest.")
	overall_ranking_desc = fields.Text(string="Overall Ranking: Description",
		help="Please briefly describe the reason for your ranking.")
	recommendation = fields.Selection([('recommended', 'Recommended'),
		('not_recommended', 'Not Recommended'), ('undecided', 'Undecided')],
		select=True, string="Overall Recommendation")
	recommendation_desc = fields.Text(string="Recommendation: Description")

	@api.model
	def create(self, vals):
		vals.update({
			'name': self.env['ir.sequence'].next_by_code('visit.report.form.seq')
		})
		return super(ScoutingForm, self).create(vals)
