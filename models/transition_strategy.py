# -*- coding: utf-8 -*-

from openerp import models, fields, api

class TransitionStrategy(models.Model):
	_name = 'sparkit.transitionstrategy'

	#Basic Information
	name = fields.Char(readonly=True, compute='_get_name')
	community_id = fields.Many2one('sparkit.community', string="Community",
		domain=[('is_partnered', '=', True)])
	community_name = fields.Char(related='community_id.name')
	community_number = fields.Char(related='community_id.community_number')
	project_id = fields.Many2one('sparkit.sparkproject', string="Project", required=True)
	project_category_id = fields.Many2one(related='project_id.category_id', readonly=True,
		string="Project Category")
	project_subcategory_id = fields.Many2one(related='project_id.subcategory_id', readonly=True,
		string="Project Sub-Category")
	facilitator_id = fields.Many2one('res.users', default=lambda self: self.env.user,
		string="Facilitator")
	post_implementation_start_date = fields.Date(related='community_id.post_implementation_start_date',
		string="Post Implementation Start Date", readonly=True)

	#Project Management Training
	mt_training1 = fields.Char(string="Management Training - 1")
	mt_training2 = fields.Char(string="Management Training - 2")
	mt_training3 = fields.Char(string="Management Training - 3")
	mt_training4 = fields.Char(string="Management Training - 4")
	mt_responsibility1 = fields.Selection([('spark', 'Spark'), ('community', 'Community'),
		('other', 'Other'), ('technical_advisor', 'Technical Advisor')], select=True,
		string="Management Training Responsibility - 1")
	mt_responsibility2 = fields.Selection([('spark', 'Spark'), ('community', 'Community'),
		('other', 'Other'), ('technical_advisor', 'Technical Advisor')], select=True,
		string="Management Training Responsibility - 2")
	mt_responsibility3 = fields.Selection([('spark', 'Spark'), ('community', 'Community'),
		('other', 'Other'), ('technical_advisor', 'Technical Advisor')], select=True,
		string="Management Training Responsibility - 3")
	mt_responsibility4 = fields.Selection([('spark', 'Spark'), ('community', 'Community'),
		('other', 'Other'), ('technical_advisor', 'Technical Advisor')], select=True,
		string="Management Training Responsibility - 4")
	mt_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Training Month - 1")
	mt_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Training Month - 2")
	mt_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Training Month - 3")
	mt_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Training Month - 4")

	#management evaluation targets
	me_target1 = fields.Text(string="Management Evaluation Target - 1")
	me_target2 = fields.Text(string="Management Evaluation Target - 2")
	me_target3 = fields.Text(string="Management Evaluation Target - 3")
	me_target4 = fields.Text(string="Management Evaluation Target - 4")
	me_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Evaluation Month - 1")
	me_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Evaluation Month - 2")
	me_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Evaluation Month - 3")
	me_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Management Evaluation Month - 4")


	#Partnership
	partner1_id = fields.Many2one('res.partner', string="Name of Partner 1")
	partner2_id = fields.Many2one('res.partner', string="Name of Partner 2")
	partner3_id = fields.Many2one('res.partner', string="Name of Partner 3")
	partner4_id = fields.Many2one('res.partner', string="Name of Partner 4")
	partnership_responsibiliy1 = fields.Selection([('spark', 'Spark'),
		('community', 'Community'), ('other', 'Other'),
		('technical_advisor', 'Technical Advisor')], select=True,
		string="Partnership Responsibility - 1",
		help="Who will be responsible for developing this partnership?")
	partnership_responsibiliy2 = fields.Selection([('spark', 'Spark'),
		('community', 'Community'), ('other', 'Other'),
		('technical_advisor', 'Technical Advisor')], select=True,
		string="Partnership Responsibility - 2",
		help="Who will be responsible for developing this partnership?")
	partnership_responsibiliy3 = fields.Selection([('spark', 'Spark'),
		('community', 'Community'), ('other', 'Other'),
		('technical_advisor', 'Technical Advisor')], select=True,
		string="Partnership Responsibility - 3",
		help="Who will be responsible for developing this partnership?")
	partnership_responsibiliy4 = fields.Selection([('spark', 'Spark'),
		('community', 'Community'), ('other', 'Other'),
		('technical_advisor', 'Technical Advisor')], select=True,
		string="Partnership Responsibility - 4",
		help="Who will be responsible for developing this partnership?")
	partnership_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Partnership Month Number - 1",
		help="When will the responsible party reach out to the partner?")
	partnership_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Partnership Month Number - 2",
		help="When will the responsible party reach out to the partner?")
	partnership_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Partnership Month Number - 3",
		help="When will the responsible party reach out to the partner?")
	partnership_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Partnership Month Number - 4",
		help="When will the responsible party reach out to the partner?")

	#Pillar Training
	pillar_training1_id = fields.Char(string="Pillar Training 1")
	pillar_training2_id = fields.Char(string="Pillar Training 2")
	pillar_training3_id = fields.Char(string="Pillar Training 3")
	pillar_training4_id = fields.Char(string="Pillar Training 4")
	pillar_training1_desc = fields.Text(string="Pillar Training 1: Description")
	pillar_training2_desc = fields.Text(string="Pillar Training 2: Description")
	pillar_training3_desc = fields.Text(string="Pillar Training 3: Description")
	pillar_training4_desc = fields.Text(string="Pillar Training 4: Description")
	pillar_training_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Pillar Training Month Number - 1")
	pillar_training_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Pillar Training Month Number - 2")
	pillar_training_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Pillar Training Month Number - 3")
	pillar_training_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Pillar Training Month Number - 4")

	#PM&E Collection & Discussion
	pme_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="PM&E Month 1")
	pme_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="PM&E Month 2")
	pme_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="PM&E Month 3")
	pme_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="PM&E Month 4")

	#By Law Review
	bylaw_review_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="By-law Review Month 1")
	bylaw_review_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="By-law Review Month 2")
	bylaw_review_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="By-law Review Month 3")
	bylaw_review_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="By-law Review Month 4")

	#Leadership Review
	leadership_review_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Leadership Review Month 1")
	leadership_review_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Leadership Review Month 2")
	leadership_review_month3 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Leadership Review Month 3")
	leadership_review_month4 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Leadership Review Month 4")

	#Leadership Re-election
	leadership_reelection_month1 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Leadership Re-election Month 1")
	leadership_reelection_month2 = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
		('5', '5'), ('6', '6'), ('8', '8'), ('10', '10'), ('12', '12'), ('15', '15'),
		('18', '18'), ('21', '21'), ('24', '24')], select=True,
		string="Leadership Re-election Month 2")

	#Meeting Dates
	meeting1 = fields.Date(string="Meeting 1 Date")
	meeting2 = fields.Date(string="Meeting 2 Date")
	meeting3 = fields.Date(string="Meeting 3 Date")
	meeting4 = fields.Date(string="Meeting 4 Date")
	meeting5 = fields.Date(string="Meeting 5 Date")
	meeting6 = fields.Date(string="Meeting 6 Date")
	meeting7 = fields.Date(string="Meeting 7 Date")
	meeting8 = fields.Date(string="Meeting 8 Date")
	meeting9 = fields.Date(string="Meeting 9 Date")
	meeting10 = fields.Date(string="Meeting 10 Date")
	meeting11 = fields.Date(string="Meeting 11 Date")
	meeting12 = fields.Date(string="Meeting 12 Date")
	meeting13 = fields.Date(string="Meeting 13 Date")

	#Static Activities
	static_activities_month1 = fields.Text(string="Static Activities Month 1",
		default="Develop Transition Strategy, Ongoing Community Assessment")
	static_activities_month2 = fields.Text(string="Static Activities Month 2",
		default="Finalize Transition Strategy")
	static_activities_month6 = fields.Text(string="Static Activities Month 6",
		default="Transition Strategy Check-in, Ongoing Community Assessment")
	static_activities_month8 = fields.Text(string="Static Activities Month 8",
		default="Review of Goals and Objectives")
	static_activities_month10 = fields.Text(string="Static Activities Month 10",
		default="Brainstorm new Goals and Objectives")
	static_activities_month12 = fields.Text(string="Static Activities Month 12",
		default="Transition Strategy Check-in, Community Assessment")
	static_activities_month18 = fields.Text(string="Static Activities Month 18",
		default="Transition Strategy Check-in, Ongoing Community Assessment")
	static_activities_month24 = fields.Text(string="Static Activities Month 24",
		default="Transition Strategy Check-in, Community Assessment")

	@api.multi
	@api.depends('community_name', 'community_number')
	def _get_name(self):
		for r in self:
			if r.project_id:
				r.name = "TS" + r.community_number + ": " + r.community_name
