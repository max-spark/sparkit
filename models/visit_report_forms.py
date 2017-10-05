# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import ValidationError, Warning



#TODO How to handle cases where it's over 3 hours? For mtg duration..
#TODO How to automatically fill in program manager?
#TODO Automatic Calculation for Next visit Date

	#---------------------------------------------------------------------
	#                      Community Visit Report Form
	#---------------------------------------------------------------------

class VisitReportForm(models.Model):
	_name = 'sparkit.vrf'
	_inherit = 'mail.thread'

	# States
	state = fields.Selection([
		('planned', 'Planned'),
		('visited', 'Visited'),
		('approved', 'Approved'),
		('cancelled', 'Cancelled'),
		], string="State", select=True, default='planned',
		track_visibility='onchange')

	#Basic Information
	name = fields.Char(String="Form ID", readonly=False, track_visibility='always',
		compute='_get_name')
	community_id = fields.Many2one('sparkit.community', string="Community",
		required=True, track_visibility='always', ondelete='cascade')
	is_group_tracking_enabled = fields.Boolean(related='community_id.is_group_tracking_enabled')
	community_number = fields.Char(related='community_id.community_number')
	community_name = fields.Char(related='community_id.name', store=True)
	facilitator_id = fields.Many2one('res.users', default=lambda self: self.env.user,
		string="Facilitator", track_visibility='onchange')
	co_facilitator_id = fields.Many2one('res.users',
		string="Co-Facilitator", track_visibility='onchange')
	m_e_assistant_id = fields.Many2one('res.users', string="M&E Assistant")
	program_manager_id = fields.Many2one('res.users', string="Program Manager")

	form_type = fields.Char(string="Form Type", compute='_get_form_type', store=True)
	visit_date = fields.Date(string="Date of Visit", required=True,
		track_visibility='onchange')
	phase = fields.Selection([
		('community_identification', 'Community Identification'),
		('planning', 'Planning'),
		('implementation', 'Implementation'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated')
		], required=True, select=True, string="Phase", track_visibility='onchange')
	step_id = fields.Many2one('sparkit.fcapstep', string="Step", track_visibility='onchange',
		required=False, domain="[('is_active', '=', True)]")
	gps_latitude = fields.Char(string="Latitude", track_visibility='onchange')
	gps_longitude = fields.Char(string="Longitude", track_visibility='onchange')
	visit_type = fields.Selection([
		('community_meeting', 'Meeting - Community Meeting'),
		('committee_meeting', 'Meeting - Committee Meeting'),
		('meeting_other', 'Meeting - Other'),
		('visit_implementation', 'Visit - Implementation'),
		('visit_post_implementation', 'Visit - Post Implementation'),
		], select=True, string="Visit Type", track_visibility='onchange')
	missed_meeting_type = fields.Selection([
		('no_meeting_visit', 'No Meeting or Visit'),
		('no_meeting_phone_call', 'No Meeting or Visit - Phone Call')
		], select=True, string="Visit Type: Missed Meeting", track_visibility='onchange')
	missed_meeting_reason = fields.Many2one('sparkit.missedmeetingreason',
		string="Reason For Missed Meeting")
	missed_meeting_text = fields.Text(string="Reason for Missed Meeting Description")

	# Dashboard Info
	phase_name = fields.Char(compute='_get_phase_name', string="Phase Name", store=True)
	state_name = fields.Char(compute='_get_state_name', string="State Name", store=True)
	visit_date_week = fields.Char(compute='get_visit_date_week', store=True)


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

	attendance_females = fields.Integer(string="Female Attendance",
		track_visibility='onchange')
	attendance_female_leaders = fields.Integer(string="Female Leaders in Attendance",
		track_visibility='onchange')
	attendance_first_time = fields.Integer(string="First Time Attendees",
		help="How many attendees attended a Spark meeting for the first time?",
		track_visibility='onchange')
	attendance_males = fields.Integer(string="Male Attendance",
		track_visibility='onchange')
	attendance_male_leaders = fields.Integer(string="Male Leaders in Attendance",
		track_visibility='onchange')
	attendance_total = fields.Integer(string="Total Attendance",
		compute='_total_attendance', track_visibility='onchange')
	attendance_relm_verified = fields.Integer(string="Attendance - RELM Verified",
		track_visibility='onchange', default="")

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

	speakers_female = fields.Integer(string="Female Speakers",
		track_visibility='onchange')
	speakers_first_time = fields.Integer(string="First Time Speakers",
		help="How many attendees spoke at a Spark meeting for the first time?",
		track_visibility='onchange')
	speakers_male = fields.Integer(string="Male Speakers",
		track_visibility='onchange')
	speakers_total = fields.Integer(string="Total Speakers",
		track_visibility='onchange', compute='_total_speakers')


	#TODO: Computing Default depending on FCAP stage? [Suggested Next visit Date]
	next_visit_date = fields.Date(string="Date of Next Visit",
		track_visibility='onchange')

	#Meeting Report
	activity1_id = fields.Many2one('sparkit.fcapactivity', string="Activity 1",
		track_visibility='onchange')
	activity2_id = fields.Many2one('sparkit.fcapactivity', string="Activity 2",
		track_visibility='onchange')
	activity3_id = fields.Many2one('sparkit.fcapactivity', string="Activity 3",
		track_visibility='onchange')

	activity1_accomplished = fields.Boolean(string="Community Activity 1 Accomplished?",
		help = "Was the planned activity accomplished?",
		track_visibility='onchange')
	activity2_accomplished = fields.Boolean(string="Community Activity 2 Accomplished?",
		track_visibility='onchange',
		help = "Was the planned activity accomplished?")
	activity3_accomplished = fields.Boolean(string="Community Activity 3 Accomplished?",
		track_visibility='onchange',
		help = "Was the planned activity accomplished?")
	activity1_desc = fields.Text(string="Activity 1 Status Description",
		track_visibility='onchange',
		help = "What activity did you plan to do with the community?")
	activity2_desc = fields.Text(string="Activity 2 Status Description",
		track_visibility='onchange',
		help = "What activity did you plan to do with the community?")
	activity3_desc = fields.Text(string="Activity 3 Status Description",
		track_visibility='onchange',
		help = "What activity did you plan to do with the community?")
	visit_duration = fields.Selection(
		[('not_applicable', 'Not Applicable'),
		 ('thirty_minutes', '30 minutes'),
		 ('one_hour', '1 hour'),
		 ('one_hour_thirty', '1 hour 30 minutes'),
		 ('two_hours', '2 hours'),
		 ('two_hours_thirty', '2 hours 30 minutes'),
		 ('three_hours', '3 hours'),
		 ('over_three_hours', 'More than 3 hours')], select=True, string="Visit Duration",
		 track_visibility='onchange',
		  help="Please enter the duration of the meeting. Please round up to nearest 15mn interval")
	visit_duration_minutes = fields.Integer(string="Visit Duration Minutes",
		track_visibility='onchange',
		compute='_visit_duration_minutes')
	travel_duration = fields.Selection(
		[('not_applicable', 'Not Applicable'),
		 ('thirty_minutes', '30 minutes'),
		 ('one_hour', '1 hour'),
		 ('one_hour_thirty', '1 hour 30 minutes'),
		 ('two_hours', '2 hours'),
		 ('two_hours_thirty', '2 hours 30 minutes'),
		 ('three_hours', '3 hours'),
		 ('over_three_hours', 'More than 3 hours')], select=True,
		 track_visibility='onchange',
		 string="One-Way Travel Duration", help="Please enter the ONE-WAY duration of travel")
	travel_duration_minutes = fields.Integer(string="Travel Duration Minutes",
		track_visibility='onchange',
		compute='_travel_duration_minutes')
	meeting_started_on_time = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('N/A', 'N/A')],
		select=True, string="Meeting Started on Time?")
	meeting_late_reason = fields.Many2one('sparkit.missedmeetingreason',
		string="Reason Meeting Delayed",
		help="Please choose the reason the meeting did not start on time.")
	meeting_started_on_time_desc = fields.Text(
		string="Meeting Started on Time: Description",
		track_visibility='onchange',
		help = "If the meeting did not start on time, please explain why.")
	cmty_set_agenda = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True,
		 track_visibility='onchange', string="Community Set Agenda")
	number_members_showing_leadership = fields.Integer(
		string="Number of Members Showing Leadership", track_visibility='onchange',
		help="Please enter the number of members that have shown leadership in the meeting.")
	conflicts_in_meeting = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], select=True, string="Conflict(s) in meeting?",
	 	track_visibility='onchange',
	 	help="Did any conflicts or challenges take place during the meeting?")
	conflicts_in_meeting_desc = fields.Text(string="Conflict(s) in Meeting: Description",
		track_visibility='onchange',
		help="Please describe any conflicts or challenges that took place during the meeting. Note whether they were resolved or not during the meeting.")
	conflicts_in_meeting_resolved = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('unknown', 'Unknown')], select=True, string="Conflict(s) in meeting: resolved?",
		 track_visibility='onchange',
		 help="During the meeting, if attendees faced any conflicts or challenges, were any of these resolved?")

	#Community Report
	cmty_reported_conflicts = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not applicable'),
		 ('unknown', 'Unknown')], string="Community Reported Conflict(s)?",
		 track_visibility='onchange',
		 help="Did the community report that it faced a conflict or challenge, which took place before or outside of the meeting?")
	cmty_reported_conflicts_desc = fields.Text(
		string="Community Reported Conflict(s): Description",
		track_visibility='onchange',
		help="Please describe the conflict or challenge the community faced, including the issue or event, who was involved, whether it was resolved, how it was resolved, and who was involved in its resolution.")
	cmty_reported_conflicts_resolved = fields.Selection(
		[('yes', 'Yes'),
		 ('no', 'No'),
		 ('not_applicable', 'Not Applicable'),
		 ('unknwon', 'Unknown')], string="Community Reported Conflict(s): resolved?",
		 track_visibility='onchange',
		 help="Did the community report that it resolved a conflict or challenge, which took place before or outside of the meeting?")

	community_highlights = fields.Text(string="Community Highlights",
		track_visibility='onchange',
		help="Please enter any highlights or other comments from your visit today.")

	#CVRF Specific Fields - (Homework)
	homework_type = fields.Selection([
		('community_building_activity', 'Community Building Activity'),
		('goal_setting_activity', 'Goal Setting Activity'),
		('gathering_information', 'Gathering Information'),
		('proposal_question', 'Proposal Question'),
		('advocacy', 'Advocacy')], track_visibility='onchange',
		select=True, string="Homework Type")
	homework_attempted_completed = fields.Boolean(
		string="Homework attempted or completed?", track_visibility='onchange')
	homework_desc = fields.Text(string="Homework Description", track_visibility='onchange')

	#IVRF/PIVRF Specific Fields
	leadership_reported_finances = fields.Selection([('1', 'Yes'),
		('0', 'No'), ('99', 'Not applicable')], select=True,
		track_visibility='onchange',
		string="Did the community leaders provide a financial update at/during meeting?",
		help="Financial updates should be a regular agenda topic and should include updates on MicroGrant status such as new items purchases, if money was drawn from account, bank account balance, MG spent thus far, cash book updates, any updates from previous week (items higher/lower than budgeted), etc.")
	leadership_presented_updated_cashbook = fields.Selection([('1', 'Yes'),
		 ('0', 'No'), ('99', 'Not applicable')], select=True,
		 track_visibility='onchange',
		 string="Did the community leaders/committee present an updated (current) cash book?",
		 help="Updated cashbook means there are consistent entries that align with activities in a community.  For example, if you are reviewing a cash book and the last entry was one month ago when the community has been actively buying items, the cash book would not be considered updated.")
	leadership_presented_accurate_cashbook = fields.Selection([('1', 'Yes'),
		 ('0', 'No'), ('99', 'Not applicable')], select=True,
		 track_visibility='onchange',
		 string="Did the community leaders/committee present an accurate cash book?",
		 help="Accurate means there are consistent entries that align with activities in a community.  For example, if you are reviewing a cash book and the entry on what the community bought was incorrect , the cash book would not be considered accurate.")
	knowledge_of_community_funds = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'), ('99', 'Not applicable')], select=True,
		 track_visibility='onchange',
		 string="Do community members have current and accurate knowledge of community funds?",
		 help="Community members should have a general awareness of MG size, how much has been spent, and how much is their bank account.")
	updated_accurate_receipts = fields.Selection([('yes', 'Yes'),
		 ('no', 'No'), ('99', 'Not applicable')], select=True,
		 track_visibility='onchange',
		 string="Does the community have accurate, complete, and high quality receipts per the disbursement schedule?",
		 help="Ensure the receipts are valid, aligned with budget items, and that the community is not just using Spark receipts for all purchased (which should be a last option). Please remember the quality of receipts is as important as having the receipts.")
	financial_update_desc = fields.Text(string="Financial A/T Description")

	#PIVRF Specific Fields
	any_new_risks = fields.Boolean(string="Any New Risks?", track_visibility='onchange')
	any_new_risks_desc = fields.Text(string="Any New Risks: Description", track_visibility='onchange')
	records_updated = fields.Boolean(string="Records Updated?", track_visibility='onchange')
	records_updated_desc = fields.Text(string="Records Updated: Description", track_visibility='onchange')

	cmty_meeting_frequency = fields.Selection([('weekly', 'Meeting Once a Week or More'),
		('monthly', 'Once a Month'), ('bimonthly', 'Twice a Month'),
		('irregularly', 'Meeting Irregularly but Frequently'),
		('ocasionally', 'Meeting Ocasionally'), ('not_meeting', 'Not Meeting')],
		track_visibility='onchange',
		select=True, string="Community Meeting Frequency")

	#Next Meeting Activities
	next_meeting_activity1_id = fields.Many2one('sparkit.fcapactivity', string="Next Meeting Activity 1",
		track_visibility='onchange')
	next_meeting_activity2_id = fields.Many2one('sparkit.fcapactivity', string="Next Meeting Activity 2",
		track_visibility='onchange')
	next_meeting_activity3_id = fields.Many2one('sparkit.fcapactivity', string="Next Meeting Activity 3",
		track_visibility='onchange')

	# Community Meeting Photo
	cmty_meeting_photo = fields.Binary(string="Community Meeting Photo")
	cmty_meeting_photo_name = fields.Char(string="Community Meeting Photo Name")

	# Migration notes
	migrated_from_sf_mf1 = fields.Boolean(string="Form from SalesForce Monitoring Forms v1?")
	migrated_from_sf_mf2 = fields.Boolean(string="Form from SalesForce Monitoring Forms v2?")
	sf_mf2_old_step = fields.Char(string="Old Step (from Salesforce)")
	migration_notes = fields.Text(string="Migration Notes")
	sf_mf2_activity1 = fields.Char(string="Old Activity1 (from Salesforce)")
	sf_mf2_activity2 = fields.Char(string="Old Activity2 (from Salesforce)")
	sf_mf2_activity3 = fields.Char(string="Old Activity3 (from Salesforce)")
	sf_mf2_next_meeting_activity1 = fields.Char(string="Old Next Meeting Activity1 (from SF)")
	sf_mf2_next_meeting_activity2 = fields.Char(string="Old Next Meeting Activity2 (from SF)")
	sf_mf2_next_meeting_activity3 = fields.Char(string="Old Next Meeting Activity3 (from SF)")
	attendance_total_mf1 = fields.Integer(string="Monitoring Forms v1 Meeting Attendance (TOTAL ONLY)")
	speakers_total_mf1 = fields.Integer(string="Monitoring Forms v1 Speakers (TOTAL ONLY)")
	leaders_total_mf1 = fields.Integer(string="Monitoring Forms v1 Leaders (TOTAL ONLY)")

	@api.depends('visit_date')
	def get_visit_date_week(self):
		for r in self:
			if r.visit_date:
				next_visit_date = datetime.strptime((str(r.visit_date)), '%Y-%m-%d').date()
				r.visit_date_week = next_visit_date.strftime("%W")

	@api.one
	@api.depends('phase')
	def _get_phase_name(self):
		for r in self:
			if r.phase:
				r.phase_name = dict(self.fields_get(allfields=['phase'])['phase']['selection'])[self.phase]

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
			elif r.visit_duration == 'thirty_minutes':
				r.visit_duration_minutes == 30
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
			elif r.travel_duration == 'thirty_minutes':
				r.travel_duration_minutes == 30
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

	@api.depends('community_id', 'visit_date')
	def _get_name(self):
		for r in self:
			if r.community_number and r.community_name:
				if r.visit_date:
					r.name = r.community_number + ': ' + r.community_id.name + ': ' + r.visit_date

	@api.depends('community_id')
	def _get_phase(self):
		for r in self:
			if r.community_id.phase:
				r.phase = r.community_id.phase_name

	@api.multi
	@api.depends('community_id')
	def _get_step(self):
		for r in self:
			if r.community_id.state:
				r.state = r.community_id.state_name

	# Assigning current M&E and Program Manager to record
	@api.model
	def create(self, vals):
		new_record = super(VisitReportForm, self).create(vals)
		new_record.m_e_assistant_id = new_record.community_id.m_e_assistant_id
		new_record.program_manager_id = new_record.community_id.program_manager_id
		return new_record

	# Workflow start: planned visit
	@api.multi
	def action_planned(self):
		self.state = 'planned'

	# Planned -> Visited
	@api.multi
	def action_visited(self):
		self.state = 'visited'

	# Planned -> Cancelled
	@api.multi
	def action_cancelled(self):
		self.state = 'cancelled'

	# Visited -> Approved
	@api.multi
	def action_approved(self):
		self.state = 'approved'


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
		 ('thirty_minutes', '30 minutes'),
		 ('one_hour', '1 hour'),
		 ('one_hour_thirty', '1 hour 30 minutes'),
		 ('two_hours', '2 hours'),
		 ('two_hours_thirty', '2 hours 30 minutes'),
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
			elif r.duration == 'thirty_minutes':
				r.duration_minutes == 30
			##How should we handle this case?
			elif r.duration == 'over_three_hours':
				r.duration_minutes = 210
			else:
				r.duration_minutes = 0

	#---------------------------------------------------
	#           Missed Meeting Reasons                 |
	#---------------------------------------------------

class MissedMeetingReason(models.Model):
	_name = 'sparkit.missedmeetingreason'

	name = fields.Char(string="Reason")
	type = fields.Selection([
		('internal', 'Internal'),
		('external_cmty', 'External - Community'),
		('external_other', 'External - Other')], select=True, string="Type", required=True)
