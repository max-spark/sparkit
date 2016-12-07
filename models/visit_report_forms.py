# -*- coding: utf-8 -*-

from openerp import models, fields, api

#TODO How to handle cases where it's over 3 hours? For mtg duration..
#TODO How to automatically fill in program manager?
#TODO Automatic Calculation for Next visit Date

	#---------------------------------------------------------------------
	#                      Community Visit Report Form
	#---------------------------------------------------------------------

class VisitReportForm(models.Model):
	_name = 'sparkit.vrf'

	#Basic Information
	name = fields.Char(String="Form ID", readonly=True)
	community_id = fields.Many2one('sparkit.community', string="Community",
		required=True, domain=[('is_partnered', '=', True)])
	community_number = fields.Char(related='community_id.community_number')
	community_name = fields.Char(related='community_id.name', store=True)
	facilitator_id = fields.Many2one('res.users', default=lambda self: self.env.user,
		string="Facilitator")
	form_type = fields.Char(string="Form Type", compute='_get_form_type', store=True)
	program_manager_id = fields.Many2one('res.users', string="Program Manager")
	visit_date = fields.Date(string="Date of Visit", required=True)
	phase = fields.Selection([('planning', 'Planning'),
		('implementation', 'Implementation'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated'),
		('community_identification', 'Community Identification'),
		('partnership_ended', 'Partnership Ended')], select=True, string="Phase")
	step_id = fields.Many2one('sparkit.fcapstep', string="FCAP Step")

	#Attendance Information
	attendance_type1_id = fields.Many2one('sparkit.grouptracking',
		string="Attendance Type 1")
	attendance_type2_id = fields.Many2one('sparkit.grouptracking',
		string="Attendance Type 2")
	attendance_type3_id = fields.Many2one('sparkit.grouptracking',
		string="Attendance Type 3")
	attendance_type4_id = fields.Many2one('sparkit.grouptracking',
		string="Attendance Type 4")
	attendance1_total = fields.Integer(string="Total Attendance Type 1")
	attendance2_total = fields.Integer(string="Total Attendance Type 2")
	attendance3_total = fields.Integer(string="Total Attendance Type 3")
	attendance4_total = fields.Integer(string="Total Attendance Type 4")
	attendance_females = fields.Integer(string="Female Attendance")
	attendance_female_leaders = fields.Integer(string="Female Leaders in Attendance")
	attendance_first_time = fields.Integer(string="First Time Attendees",
		help="How many attendees attended a Spark meeting for the first time?")
	attendance_males = fields.Integer(string="Male Attendance")
	attendance_male_leaders = fields.Integer(string="Male Leaders in Attendance")
	attendance_total = fields.Integer(string="Total Attendance", compute='_total_attendance')

	#Speaker information
	speakers_type1_id = fields.Many2one('sparkit.grouptracking',
		string="Speakers Type 1")
	speakers_type2_id = fields.Many2one('sparkit.grouptracking',
		string="Speakers Type 2")
	speakers_type3_id = fields.Many2one('sparkit.grouptracking',
		string="Speakers Type 3")
	speakers_type4_id = fields.Many2one('sparkit.grouptracking',
		string="Speakers Type 4")
	speakers1_total = fields.Integer(string="Total Speakers Type 1")
	speakers2_total = fields.Integer(string="Total Speakers Type 2")
	speakers3_total = fields.Integer(string="Total Speakers Type 3")
	speakers4_total = fields.Integer(string="Total Speakers Type 4")
	speakers_female = fields.Integer(string="Female Speakers")
	speakers_first_time = fields.Integer(string="First Time Speakers",
		help="How many attendees spoke at a Spark meeting for the first time?")
	speakers_male = fields.Integer(string="Male Speakers")
	speakers_total = fields.Integer(string="Total Speakers", compute='_total_speakers')

	#Next Meeting Information
	next_meeting_category1_id = fields.Many2one('sparkit.fcapcategory',
		string="Next Meeting Category 1")
	next_meeting_category2_id = fields.Many2one('sparkit.fcapcategory',
		string="Next Meeting Category 2")
	next_meeting_category3_id = fields.Many2one('sparkit.fcapcategory',
		string="Next Meeting Category 3")
	next_meeting_activity1_id = fields.Many2one('sparkit.fcapactivity',
		string="Next Meeting Activity 1")
	next_meeting_activity2_id = fields.Many2one('sparkit.fcapactivity',
		string="Next Meeting Activity 2")
	next_meeting_activity3_id = fields.Many2one('sparkit.fcapactivity',
		string="Next Meeting Activity 3")

	# Computing Default depending on FCAP stage? [Suggested Next visit Date]
	next_visit_date = fields.Date(string="Date of Next Visit")

	#Meeting Report
	activity_category1_id = fields.Many2one('sparkit.fcapcategory',
		string="Activity Category 1")
	activity_category2_id = fields.Many2one('sparkit.fcapcategory',
		string="Activity Cateogry 2")
	activity_category3_id = fields.Many2one('sparkit.fcapcategory',
		string="Activity Category 3")
	activity1_id = fields.Many2one('sparkit.fcapactivity', string="Activity 1")
	activity2_id = fields.Many2one('sparkit.fcapactivity', string="Activity 2")
	activity3_id = fields.Many2one('sparkit.fcapactivity', string="Activity 3")

	activity1_accomplished = fields.Boolean(string="Community Activity 1 Accomplished?",
		help = "Was the planned activity accomplished?")
	activity2_accomplished = fields.Boolean(string="Community Activity 2 Accomplished?",
		help = "Was the planned activity accomplished?")
	activity3_accomplished = fields.Boolean(string="Community Activity 3 Accomplished?",
		help = "Was the planned activity accomplished?")
	activity1_desc = fields.Text(string="Activity 1 Status Description",
		help = "What activity did you plan to do with the community?")
	activity2_desc = fields.Text(string="Activity 2 Status Description",
		help = "What activity did you plan to do with the community?")
	activity3_desc = fields.Text(string="Activity 3 Status Description",
		help = "What activity did you plan to do with the community?")
	facilitation_goal = fields.Text(string="Facilitation Goal",
		help = "Was there a facilitation goal with this meeting, for example, to improve trust among community members? If so, please list here")
	facilitation_goal_accomplished = fields.Boolean(
		string="Facilitation Goal Accomplished?")
	facilitation_goal_desc = fields.Text(string="Facilitation Goal Description")
	visit_duration = fields.Selection(
		[('not_applicable', 'Not Applicable'),
		 ('one_hour', '1 hour'),
		 ('one_hour_thirty', '1 hour 30 minutes'),
		 ('two_hours', '2 hours'),
		 ('two_hours_thirty', '2 hours 30 mintutes'),
		 ('three_hours', '3 hours'),
		 ('over_three_hours', 'More than 3 hours')], select=True, string="Visit Duration",
		  help="Please enter the duration of the meeting. Please round up to nearest 15mn interval")
	visit_duration_minutes = fields.Integer(string="Visit Duration Minutes",
		compute='_visit_duration_minutes')
	travel_duration = fields.Selection(
		[('not_applicable', 'Not Applicable'),
		 ('one_hour', '1 hour'),
		 ('one_hour_thirty', '1 hour 30 minutes'),
		 ('two_hours', '2 hours'),
		 ('two_hours_thirty', '2 hours 30 mintutes'),
		 ('three_hours', '3 hours'),
		 ('over_three_hours', 'More than 3 hours')], select=True,
		 string="Travel Duration", help="Please enter the ONE-WAY duration of travel")
	travel_duration_minutes = fields.Integer(string="Travel Duration Minutes",
		compute='_travel_duration_minutes')
	meeting_started_on_time = fields.Boolean(string="Meeting Started on Time?")
	meeting_started_on_time_desc = fields.Text(
		string="Meeting Started on Time: Description",
		help = "If the meeting did not start on time, please explain why.")
	cmty_set_agenda = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True, string="Community Set Agenda?")
	cmty_set_agenda_desc = fields.Text(string="Community Set Agenda: Description")
	number_members_showing_leadership = fields.Integer(
		string="Number of Members Showing Leadership", help="""
		Please enter the number of members that have shown leadership in the meeting.""")
	conflicts_in_meeting = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True, string="Conflict(s) in meeting?",
		 	help="Please describe any conflicts or challenges that took place during the meeting. Note whether they were resolved or not during the meeting.")
	conflicts_in_meeting_desc = fields.Text(string="Conflict(s) in Meeting: Description",
		help="Please describe any conflicts or challenges that took place during the meeting. Note whether they were resolved or not during the meeting.")
	conflicts_in_meeting_resolved = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('unknown', 'Unknown')], select=True, string="Conflict(s) in meeting: resolved?",
		 help="During the meeting, if attendees faced any conflicts or challenges, were any of these resolved?")

	#Community Trainings linking to training configuration table
	training_delivered1_id = fields.Many2one('sparkit.training',
		string="Training Delivered 1",
		help="If a training was delivered during contact, please select it from the list. If more than one training was delivered, please use the field(s) below to select the other training(s) delivered.")
	training_delivered2_id = fields.Many2one('sparkit.training',
		string="Training Delivered 2", help="If a training was delivered during contact, please select it from the list. If more than one training was delivered, please use the field(s) below to select the other training(s) delivered.")
	training_delivered3_id = fields.Many2one('sparkit.training',
		string="Training Delivered 3", help="If a training was delivered during contact, please select it from the list. If more than one training was delivered, please use the field(s) below to select the other training(s) delivered.")
	training_delivered_other = fields.Text(string="Training Delivered - Other",
		help="If a training was delivered that was not listed above, please describe the training here.")
	training_delivered_desc1 = fields.Text(string="Training Description 1")
	training_delivered_desc2 = fields.Text(string="Training Description 2")
	training_delivered_desc3 = fields.Text(string="Training Description 3")
	training_needed = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No')], string="Training Needed?")
	training_needed1_id = fields.Many2one('sparkit.training', string="Training Needed 1")
	training_needed2_id = fields.Many2one('sparkit.training', string="Training Needed 2")
	training_needed3_id = fields.Many2one('sparkit.training', string="Training Needed 3")
	training_needed_desc1 = fields.Text(string="Training Needed 1: Description")
	training_needed_desc2 = fields.Text(string="Training Needed 2: Description")
	training_needed_desc3 = fields.Text(string="Training Needed 3: Description")
	training_needed_other = fields.Text(string="Training Needed - Other")

	#Community Report
	cmty_reported_conflicts = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], string="Community Reported Conflict(s)?",
		 help="Did the community report that it faced a conflict or challenge, which took place before or outside of the meeting?")
	cmty_reported_conflicts_desc = fields.Text(
		string="Community Reported Conflict(s): Description",
		help="Please describe the conflict or challenge the community faced, including the issue or event, who was involved, whether it was resolved, how it was resolved, and who was involved in its resolution.")
	cmty_reported_conflicts_resolved = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('unknwon', 'Unknown')], string="Community Reported Conflict(s): resolved?",
		 help="Did the community report that it resolved a conflict or challenge, which took place before or outside of the meeting?")

	#Communications
	quotes_from_communtiy_members = fields.Text(string="Quotes from Community Members")
	ideas_for_social_media = fields.Text(string="Ideas for Social Media")
	story_collection=fields.Text(string="Story Collection")

	#Independent Project Updates
	independent_project_update_ids = fields.One2many(related='community_id.independent_project_update_ids')

	#Savings Group Updates
	savings_group_update_ids = fields.One2many(related='community_id.savings_group_update_ids')

	#Independent Meetings
	independent_meeting_ids = fields.One2many(related='community_id.independent_meeting_ids')

	#Project Support Initiative Updates
	project_support_initiative_ids = fields.One2many(related='community_id.project_support_initiative_ids')

	#Advocacy Updates
	partnership_update_ids = fields.One2many(related='community_id.partnership_update_ids')

	#Pilot Updates
	pilot_update_ids = fields.One2many(related='community_id.pilot_update_ids')

	#CVRF Specific Fields - (Homework)
	homework_type = fields.Selection([
		('community_building_activity', 'Community Building Activity'),
		('goal_setting_activity', 'Goal Setting Activity'),
		('gathering_information', 'Gathering Information'),
		('proposal_question', 'Proposal Question'),
		('advocacy', 'Advocacy')], select=True, string="Homework Type")
	homework_attempted_completed = fields.Boolean(
		string="Homework attempted or completed?")
	homework_desc = fields.Text(string="Homework Description")

	#IVRF/PIVRF Specific Fields
	all_receipts_present = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True, string="All Receipts Present?")
	all_receipts_present_desc = fields.Text(string="All Receipts Present: Description")
	bank_deposits = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True, string="Bank Deposits")
	cashbook_updated = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True, string="Cashbook Updated")
	cashbook_updated_desc = fields.Text(string="Cashbook Updated: Description")
	cmty_discussed_budget = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 string="Community Discussed Budget in Meeting")
	cmty_discussed_budget_desc = fields.Text(
		string="Community Discussed Budget in Meeting: Description")
	cmty_meeting_deadines = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 string="Community Meeting Deadlines?")
	knowledge_of_community_funds = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 string="Knowledge of Community Funds?")
	knowledge_of_community_funds_desc = fields.Text(
		string="Knowledge of Community Funds: Description")
	leadership_presented_bankslips = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 string="Leadership Presented Bankslips")
	leadership_presented_bankslips_desc = fields.Text(
		string="Leadership Presented Bankslips: Description")
	leadership_presented_cashbook = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 string="Leadership Presented Cashbook")
	leadership_presented_cashbook_desc = fields.Text(
		string="Leadership Presented Cashbook: Description")
	leadership_reported_finances = fields.Boolean(
		string="Leadership Reported on Finances")
	leadership_reported_finances_desc = fields.Text(
		string="Leadership Reported on Finances: Description")
	noncommittee_cashbook_review = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 string="Non-Committee Cashbook Review")
	noncommittee_cashbook_review_desc = fields.Text(
		string="Non-Committee Cashbook Review: Description")
	project_on_budget = fields.Selection([('under', 'Under Budget'),
		('over', 'Over Budget'),
		('on', 'On Budget')], select=True, string="Project on Budget")

	#PIVRF Specific Fields
	any_new_risks = fields.Boolean(string="Any New Risks?")
	any_new_risks_desc = fields.Text(string="Any New Risks: Description")
	records_updated = fields.Boolean(string="Records Updated?")
	records_updated_desc = fields.Text(string="Records Updated: Description")

	cmty_meeting_frequency = fields.Selection([('weekly', 'Meeting Once a Week or More'),
		('monthly', 'Once a Month'), ('bimonthly', 'Twice a Month'),
		('irregularly', 'Meeting Irregularly but Frequently'),
		('ocasionally', 'Meeting Ocasionally'), ('not_meeting', 'Not Meeting')],
		select=True, string="Community Meeting Frequency")

	@api.depends('phase')
	def _get_form_type(self):
		for r in self:
			if r.phase:
				if r.phase == 'planning':
					r.form_type = "CVRF"
				elif r.phase == 'community_identification':
					r.form_type = "CIVRF"
				elif r.phase == 'implementation':
					r.form_type = "IVRF"
				elif r.phase == 'post_implementation':
					r.form_type = "PIVRF"
				elif r.phase == 'graduated':
					r.form_type = "PIVRF"

	@api.depends('visit_duration')
	def _visit_duration_minutes(self):
		for r in self:
			if r.visit_duration == 'one_hour':
				r.visit_duration_minutes = 60
			elif r.visit_duration == 'one_hour_thirty':
				r.visit_duration_minutes = 90
			elif r.visit_duration == 'two_hours':
				r.visit_duration_minutes = 120
			elif r.visit_duration == 'two_hours_thirty':
				r.visit_duration_minutes = 150
			elif r.visit_duration == 'three_hours':
				r.visit_duration_minutes = 180
			##How should we handle this case?
			elif r.visit_duration == 'over_three_hours':
				r.visit_duration_minutes = 210
			else:
				r.visit_duration_minutes = 0


	@api.depends('travel_duration')
	def _travel_duration_minutes(self):
		for r in self:
			if r.travel_duration == 'one_hour':
				r.travel_duration_minutes = 60
			elif r.travel_duration == 'one_hour_thirty':
				r.travel_duration_minutes = 90
			elif r.travel_duration == 'two_hours':
				r.travel_duration_minutes = 120
			elif r.travel_duration == 'two_hours_thirty':
				r.travel_duration_minutes = 150
			elif r.travel_duration == 'three_hours':
				r.travel_duration_minutes = 180
			##How should we handle this case?
			elif r.travel_duration == 'over_three_hours':
				r.travel_duration_minutes = 210
			else:
				r.travel_duration_minutes = 0

	@api.depends('speakers_male', 'speakers_female')
	def _total_speakers(self):
		for r in self:
			r.speakers_total = r.speakers_female + r.speakers_male

	@api.depends('attendance_males', 'attendance_females')
	def _total_attendance(self):
		for r in self:
			r.attendance_total = r.attendance_males + r.attendance_females

	@api.model
	def create(self, vals):
		vals.update({
			'name': self.env['ir.sequence'].next_by_code('visit.report.form.seq')
		})
		return super(VisitReportForm, self).create(vals)




	#---------------------------------------------------
	#                    Trainings 	                   |
	#---------------------------------------------------

class Training(models.Model):
	_name = 'sparkit.training'

	name = fields.Char(string="Training")

	#---------------------------------------------------
	#               Group Tracking                     |
	#---------------------------------------------------

class GroupTracking(models.Model):
	_name = 'sparkit.grouptracking'

	name = fields.Char(string="Groups")

	#---------------------------------------------------
	#             Independent Meetings                 |
	#---------------------------------------------------

class IndependentMeeting(models.Model):
	_name = 'sparkit.independentmeeting'

	name = fields.Char(compute='_get_name')
	community_id = fields.Many2one('sparkit.community', string="Community")
	attendance = fields.Integer(string="Independent Meeting Attendance")
	date = fields.Date(string="Independent Meeting Date")
	duration = fields.Selection(
		[('not_applicable', 'Not Applicable'),
		 ('one_hour', '1 hour'),
		 ('one_hour_thirty', '1 hour 30 minutes'),
		 ('two_hours', '2 hours'),
		 ('two_hours_thirty', '2 hours 30 mintutes'),
		 ('three_hours', '3 hours'),
		 ('over_three_hours', 'More than 3 hours')], select=True,
		 string="Independent Meeting Duration",
		 help="Please enter the duration of the independent meeting. Please round up to the nearest 15 mn interval.")
	duration_minutes = fields.Integer(string="Duration Minutes", readonly=True,
		compute = '_independent_mtg_duration_minutes')

	@api.depends('duration')
	def _independent_mtg_duration_minutes(self):
		for r in self:
			if r.duration == 'one_hour':
				r.duration_minutes = 60
			elif r.duration == 'one_hour_thirty':
				r.duration_minutes = 90
			elif r.duration == 'two_hours':
				r.duration_minutes = 120
			elif r.duration == 'two_hours_thirty':
				r.duration_minutes = 150
			elif r.duration == 'three_hours':
				r.duration_minutes = 180
			##How should we handle this case?
			elif r.duration == 'over_three_hours':
				r.duration_minutes = 210
			else:
				r.duration_minutes = 0
