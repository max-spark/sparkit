# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from openerp.exceptions import ValidationError, Warning

# TODO: Automatic Important Dates
# TODO: Think about codes for partner organizations

class Community(models.Model):
	_name = 'sparkit.community'
	_inherit = 'mail.thread'

	#Basic Information
	name = fields.Char(string="Community Name", required=True, track_visibility='always')
	description = fields.Text(string="Community Description", track_visibility='onchange')
	community_number = fields.Char(string="Community Number", readonly=True)
	is_partnered = fields.Boolean(string="Partnered?", default=False, readonly=True)
	relm_counts = fields.Boolean(string="RELM Counts?", default=True)	
	facilitator_id = fields.Many2one('res.users',
		string="Facilitator",
		default=lambda self: self.env.user,
		track_visibility='onchange')
	co_facilitator_id = fields.Many2one('res.users',
		string="Co-Facilitator",
		track_visibility='onchange')
	program_manager_id = fields.Many2one('res.users', string="Program Manager",
		track_visibility='onchange')
	m_e_assistant_id = fields.Many2one('res.users', string="Monitoring/Evaluation Assistant",
		track_visibility='onchange')
	sms_sender_id = fields.Many2one('res.users', string="SMS Sender",
		track_visibility='onchange')
	is_active = fields.Boolean(string="Active?", readonly=True)
	phase_name = fields.Char(compute='_get_phase_name', string="Phase Name", store=True)
	state_name = fields.Char(compute='_get_state_name', string="State Name", store=True)
	special_cases = fields.Many2many('sparkit.specialcases', string="Special Cases",
		track_visibility='onchange')
	is_group_tracking_enabled = fields.Boolean(string="Group Tracking Enabled?")
	still_meeting = fields.Boolean(string="Community Still Meeting Independently?")
	still_meeting_enddate = fields.Date(string="Date of Last Meeting",
		help="Please enter the date of the community's last meeting.")
	project_sustaining = fields.Boolean(string="Project Sustaining?")
	project_sustaining_enddate = fields.Date(string="Date Project Stopped Sustaining",
		help="Please enter the approximate date the project stopped sustaining.")

	country_region = fields.Selection([
		('eastern_uganda', 'Eastern Uganda'),
		('northern_uganda', 'Northern Uganda')
		], track_visibility='onchange')
	proposal_link = fields.Char(string="Link to Project Proposal", track_visibility='onchange')
	secondary_proposal_link = fields.Char(string="Link to Secondary Project Proposal", track_visibility='onchange')	

	#Workflow States
	phase = fields.Selection([
		('community_identification', 'Community Identification'),
		('planning', 'Planning'),
		('implementation', 'Implementation'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated')
		], default='community_identification',
		track_visibility='onchange')

	#Planning Steps
	state = fields.Selection([
		('community_identification', 'Community Identification - Baseline'),
		('introductions', 'Introductions'),
		('partnership', 'Partnership'),
		('community_building', 'Community Building'),
		('goal_setting_goals', 'Goal Setting: Goals'),
		('goal_setting_pathways', 'Goal Setting: Pathways'),
		('implementation_plan', 'Proposal Development: Implementation Plan'),
		('operational_plan', 'Proposal Development: Operational Plan'),
		('measuring_success', 'Proposal Development: Measuring Success'),
		('sustainability_plan', 'Proposal Development: Sustainability Plan'),
		('transition_strategy', 'Proposal Development: Transition Strategy'),
		('proposal_review', 'Proposal Development: Proposal Finalization'),
		('grant_agreement', 'Implementation: Grant Agreement & Financial Management'),
		('first_disbursement', 'Implementation: Accountability & Transparency (Disbursements Begin)'),
		('leadership', 'Implementation: Leadership'),
		('imp_transition_strategy', 'Implementation: Transition Strategy'),
		('post_implementation1', 'Post Implementation: Management Support'),
		('post_implementation2', 'Post Implementation: Future Envisioning'),
		('post_implementation3', 'Post Implementation: Graduation'),
		('graduated', 'Graduated'),
		('partnership_canacelled', 'Partnership Cancelled')
	], string="Step", readonly=False, track_visibility='onchange')

	#Community Detail
	#TODO: switch this back to true
	facilitation_language = fields.Char(string="Facilitation Language",
		required=False)
	meeting_day = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'),
		('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')],
		select=True, string="Meeting Day",
		help="Please select the day you meet the community for facilitation meetings.",
		track_visibility='onchange')
	meeting_time = fields.Char(string="Meeting Time",
		track_visibility='onchange',
		help="Please input the time facilitation meetings are scheduled with the community.")
	bank_account = fields.Many2one('res.partner.bank', string="Community Bank Account",
		track_visibility='onchange')
	govt_registration_number = fields.Char(string="Government Registration Number",
		track_visibility='onchange')
	village_slogan = fields.Text(string="Community Vision",
		track_visibility='onchange')

	#dates
	date_scouted=fields.Date(string="Date Scouted", required=False,
		help="Please enter the date the community was scouted",
		track_visibility='onchange')
	partnership_date = fields.Date(string="Partnership Date",
		track_visibility='onchange')
	implementation_start_date = fields.Date(string="Implementation Start Date",
		track_visibility='onchange')
	post_implementation_start_date = fields.Date(string="Post Implementation Start Date",
		track_visibility='onchange')
	graduation_date = fields.Date(string="Graduation Date",
		track_visibility='onchange')

	#Demographics
	num_hh_community = fields.Integer(string="Number of Households",
		track_visibility='onchange', required=True)
	num_ppl_community = fields.Float(string="Number of People",
		help="This is computed using the country's average number of people per household",
		readonly=True, compute='_get_num_ppl_community')
	num_hh_in_planning_group = fields.Integer(string="Number of Households in Planning Group",
		track_visibility='onchange')
	num_ppl_in_planning_group = fields.Integer(string="Number of People in Planning Group",
		track_visibility='onchange')

	# DATA
	avg_attendance = fields.Float(string="Average Attendance (last 90 days)",
		compute='get_grad_metrics')
	avg_female_attendance = fields.Float(string="Average Female Attendance (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_female_attendance = fields.Float(string="Average Percent Female Attendance (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_participation = fields.Float(string="Average Percent Participation (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_female_participation = fields.Float(string="Average Female Participation (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_pg_participation = fields.Float(string="Average Percent Planning Group Participation (last 90 days)",
		compute='get_grad_metrics')
	avg_participation = fields.Float(string="Average Participation (last 90 days)",
		compute='get_grad_metrics')

	avg_percent_female_attendance_display = fields.Char(string="Average Percent Female Attendance (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_participation_display = fields.Char(string="Average Percent Participation (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_female_participation_display = fields.Char(string="Average Female Participation (last 90 days)",
		compute='get_grad_metrics')
	avg_percent_pg_participation_display = fields.Char(string="Average Percent Planning Group Participation (last 90 days)",
		compute='get_grad_metrics')


	#Location Information
	country_id = fields.Many2one('res.country', string="Country", required=True,
		domain=[('is_active', '=', True)], track_visibility='onchange')
	cell = fields.Char(string="Cell/Colline/Parish", track_visibility='onchange')
	district = fields.Char(string="District/Province", track_visibility='onchange')
	village = fields.Char(string="Village/Sous-Colline", track_visibility='onchange')
	sector = fields.Char(string="Sector/Commune/Sub-County", track_visibility='onchange')
	directions_to_community = fields.Text(string="Directions to Community",
		track_visibility='onchange')
	cost_to_community = fields.Float(string="Cost of Rountrip Travel to Community",
		help="Please enter how much it costs to get to the community and back in your local currency.",
		track_visibility='onchange')
	# Longitude and Latitude (to be automatically generated + entered by application)
	gps_coordinates_longitude = fields.Char(
		string="Communiy Center GPS Coordinates - Longitude",
		track_visibility='onchange')
	gps_coordinates_latitude = fields.Char(string="Communiy Center GPS Coordinates - Latitude",
		track_visibility='onchange')
	bodamoto_drivers = fields.Many2many('res.partner', 'community_ids', string="Boda/Moto Drivers",
		domain=[('company_type', '=', 'boda_moto')],
		track_visibility='onchange')

	#Location - Vulnerability Information
	clean_water_gps_coordinates_long = fields.Char("Nearest Clean Water Source - GPS Longitude")
	clean_water_gps_coordinates_lat = fields.Char("Nearest Clean Water Source - GPS Latitude")
	health_center_gps_coordinates_lat = fields.Char("Nearest Health Center - GPS Latitude")
	health_center_gps_coordinates_long = fields.Char("Nearest Health Center - GPS Longitude")
	school_gps_coordinates_long = fields.Char("Nearest School - GPS Longitude")
	school_gps_coordinates_lat = fields.Char("Nearest School - GPS Latitude")
	nearest_town_gps_coordinates_long = fields.Char("Nearest Town - GPS Longitude")
	nearest_town_gps_coordinates_lat = fields.Char("Nearest Town - GPS Latitude")

	nearest_health_center_details = fields.Text("Nearest Health Center Details")
	nearest_school_details = fields.Text("Nearest School Details")
	nearest_town_details = fields.Text("Nearest Town Details")
	nearest_clean_water_details = fields.Text("Nearest Water Access Point Details")

	#Technical Advisor
	technical_advisor_id = fields.Many2one('res.partner',
		string="Technical Advisor",
		domain=[('company_type', '=', 'technical_advisor')],
		track_visibility='onchange')
	technical_advisor_workplan = fields.Binary(string="Technical Advisor Workplan")
	ta_workplan_name = fields.Char(string="Technical Advisor Workplan Name")

	implementation_partner_facilitator_id = fields.Many2one('res.partner',
		string="Implementation Partner Facilitator",
		domain=[('company_type', '=', 'implementation_partner')],
		track_visibility='onchange')

	# Important Documents
	number_signed_partnership_agreement = fields.Integer(string="Number of People Who Signed Partnership Agreement",
		track_visibility='onchange')
	partnership_agreement_name = fields.Char(string="Partnership Agreement File Name")
	partnership_agreement = fields.Binary(string="Partnership Agreement",
		track_visibility='onchange')
	partnership_agreement_date = fields.Date(string="Partnership Agreement Signed Date")
	number_signed_grant_agreement = fields.Integer(string="Number of People Who Signed Grant Agreement",
		track_visibility='onchange')
	grant_agreement_name = fields.Char(string="Grant Agreement File Name")
	grant_agreement = fields.Binary(string="Grant Agreement", track_visibility='onchange')
	grant_agreement_signed_date = fields.Date(string="Grant Agreement Signed Date")
	number_signed_exit_agreement = fields.Integer(string="Number of People Who Signed Exit Agreement",
		track_visibility='onchange')
	exit_agreement_name = fields.Char(string="Exit Agreement File Name")
	exit_agreement = fields.Binary(string="Exit Agreement", track_visibility='onchange')
	exit_agreement_signed_date = fields.Date(string="Exit Agreement Signed Date")

	# Project Detail
	goals_ideas = fields.Integer(string="Goals - Number of Ideas",
		help="Please enter the number of ideas the community brainstormed for their goal.",
		track_visibility='onchange')
	goals_selected = fields.Text(string="Goals - Selected Goal Description",
		help="Please describe the community's chosen goal in their own words.",
		track_visibility='onchange')
	indicator1 = fields.Char(string="Indicator 1", track_visibility='onchange')
	indicator2 = fields.Char(string="Indicator 2", track_visibility='onchange')
	indicator3 = fields.Char(string="Indicator 3", track_visibility='onchange')
	indicator1_baseline = fields.Char(string="Baseline - 1", track_visibility='onchange')
	indicator2_baseline = fields.Char(string="Baseline - 2", track_visibility='onchange')
	indicator3_baseline = fields.Char(string="Baseline - 3", track_visibility='onchange')
	indicator1_6months = fields.Char(string="6 months PI - 1", track_visibility='onchange')
	indicator2_6months = fields.Char(string="6 months PI - 2", track_visibility='onchange')
	indicator3_6months = fields.Char(string="6 months PI - 3", track_visibility='onchange')
	indicator1_12months = fields.Char(string="1 year PI - 1", track_visibility='onchange')
	indicator2_12months = fields.Char(string="1 year PI - 2", track_visibility='onchange')
	indicator3_12months = fields.Char(string="1 year PI - 3", track_visibility='onchange')
	indicator1_18months = fields.Char(string="18 months PI - 1", track_visibility='onchange')
	indicator2_18months = fields.Char(string="18 months PI - 2", track_visibility='onchange')
	indicator3_18months = fields.Char(string="18 months PI - 3", track_visibility='onchange')
	indicator1_2years = fields.Char(String="2 years PI - 1", track_visibility='onchange')
	indicator2_2years = fields.Char(String="2 years PI - 2", track_visibility='onchange')
	indicator3_2years = fields.Char(String="2 years PI - 3", track_visibility='onchange')
	indicator1_6month_target = fields.Char(string="6 months PI - 1 - Target", track_visibility='onchange')
	indicator2_6month_target = fields.Char(string="6 months PI - 2 - Target", track_visibility='onchange')
	indicator3_6month_target = fields.Char(string="6 months PI - 3 - Target", track_visibility='onchange')
	indicator1_12months_target = fields.Char(string="1 year PI - 1 - Target", track_visibility='onchange')
	indicator2_12months_target = fields.Char(string="1 year PI - 2 - Target", track_visibility='onchange')
	indicator3_12months_target = fields.Char(string="1 year PI - 3 - Target", track_visibility='onchange')
	indicator1_18months_target = fields.Char(string="18 Months PI - 1 - Target", track_visibility='onchange')
	indicator2_18months_target = fields.Char(string="18 Months PI - 2 - Target", track_visibility='onchange')
	indicator3_18months_target = fields.Char(string="18 Months PI - 3 - Target", track_visibility='onchange')
	indicator1_2years_target = fields.Char(string="2 years PI - 1 - Target", track_visibility='onchange')
	indicator2_2years_target = fields.Char(string="2 years PI - 2 - Target", track_visibility='onchange')
	indicator3_2years_target = fields.Char(string="2 years PI - 3 - Target", track_visibility='onchange')


	pathways_ideas = fields.Integer(string="Pathways - Number of Ideas",
		help="Please enter the number of ideas the community brainstormed for their pathway.",
		track_visibility='onchange')
	project_description = fields.Text(string = "Pathways - Selected Pathway Description",
		help="Please describe the community's chosen project in their own words.",
		track_visibility='onchange')


	# Community Leaders
	community_leader_ids = fields.One2many('res.partner', 'community_id',
		domain=[('company_type', '=', 'community_leader')],
		track_visibility='onchange')
	# NOTE: stored in the database in order to use for reporting.
	number_female_leaders = fields.Integer(string="Number Female Leaders",
		compute='_compute_number_female_leaders',
		store=True,
		track_visibility='onchange')
	total_leaders = fields.Integer(string="Total Leaders",
		compute='_compute_total_leaders',
		store=True,
		track_visibility='onchange'
	)
	total_female_leaders_byfacilitator = fields.Integer(string="Total Number of Female Leaders",
		help="Entered by Facilitator.",
		track_visibility='onchange')
	total_male_leaders_byfacilitator = fields.Integer(string="Total Number of Male Leaders",
		help="Entered by Facilitator.",
		track_visibility='onchange')		

	# Community Facilitators
	community_facilitator_ids = fields.One2many('res.partner', 'community_id',
		domain=[('company_type', '=', 'community_facilitator')],
		track_visibility='onchange')

	# Community members
	community_member_ids = fields.One2many('res.partner', 'community_id',
		domain=[('company_type', '=', 'community_member')],
		track_visibility='onchange')

	#VRF Forms
	vrf_ids = fields.One2many('sparkit.vrf', 'community_id', string="VRFs",
		track_visibility='onchange')
	cvrf_ids = fields.One2many('sparkit.vrf', 'community_id', string="CVRFs",
		domain=[('form_type', '=', "CVRF")], track_visibility='onchange')
	ivrf_ids = fields.One2many('sparkit.vrf', 'community_id', string="IVRFs",
		domain=[('form_type', '=', "IVRF")], track_visibility='onchange')
	pivrf_ids = fields.One2many('sparkit.vrf', 'community_id', string="PIVRFs",
		domain=[('form_type', '=', "PIVRF")], track_visibility='onchange')
	number_planning_visits = fields.Integer(compute='_get_number_planning_visits',
		store=True)
	number_implementation_visits = fields.Integer(compute='_get_number_implementation_visits',
		store=True)
	number_pi_visits = fields.Integer(compute='_get_number_pi_visits',
		store=True)

	#Community Project
	spark_project_ids = fields.One2many('sparkit.sparkproject', 'community_id', string="Grant Project(s)",
		track_visibility='onchange')
	project_category_id = fields.Many2one('sparkit.projectcategory',
		string="Project Category", track_visibility='onchange')
	project_subcategory_id = fields.Many2one('sparkit.projectsubcategory',
		string="Project SubCategory", track_visibility='onchange')
	project_support_initiative_ids = fields.One2many('sparkit.projectsupportinitiative',
		'community_id', track_visibility='onchange')

	#Last Visit Date Calculations
	last_visit_date = fields.Date(string="Last Visit Date", compute='_get_visit_date')
	next_visit_date = fields.Date(string="Next Visit Date", compute='_get_visit_date', store=True)
	next_visit_date_week = fields.Char(compute='_get_visit_date', store=True)

	#Ind Projects
	independent_project_ids = fields.One2many('sparkit.independentproject',
		'community_id', string="Independent Projects", ondelete='set null',
		track_visibility='onchange')
	independent_project_update_ids = fields.One2many('sparkit.independentprojectupdate',
		'community_id', ondelete='set null')
	total_independent_projects = fields.Integer(compute='_get_number_ind_projects',
		string="Total Number of Independent Projects",
		store=True,
		track_visibility='onchange')

	#Independent Meetings
	independent_meeting_ids = fields.One2many('sparkit.independentmeeting', 'community_id', string="Independent Meetings",
		track_visibility='onchange')

	#Savings Groups
	savings_group_ids = fields.One2many('sparkit.savingsgroup', 'community_id',
		string="Savings Groups", track_visibility='onchange', ondelete='set null')
	savings_group_update_ids = fields.One2many('sparkit.savingsgroupupdate', 'community_id',
		ondelete='set null')
	number_hh_savings_group = fields.Integer(string="Number of Households in a Savings Group",
		store=True, compute='_get_number_hh_savings_group')

	#OCAs
	oca_ids = fields.One2many('sparkit.oca', 'community_id', string="OCAs", track_visibility='onchange')


	#Transition Strategy
	transition_strategy_ids = fields.One2many('sparkit.transitionstrategy', 'community_id',
		track_visibility='onchange', string="Transition Strategy")

	#Partnerships
	partnership_ids = fields.One2many('sparkit.partnership', 'community_id',
		track_visibility='onchange', string="Partnerships", ondelete='set null')
	partnership_update_ids = fields.One2many(related='partnership_ids.partnership_update_ids',
		ondelete='set null')

	#Program Reviews
	programreview_ids = fields.One2many('sparkit.programreview', 'community_id',
		track_visibility='onchange', string="Program Reviews", ondelete='set null')

	# Counting Number of Visit Report Forms
	#planning_visits = fields.Integer(string="Planning Visits",	compute='_get_num_planning_visits')


	#-----------------------------------------------------
	#-                  Workflow Fields
	#-----------------------------------------------------
	#workflow configuration
	workflow_config_id = fields.Many2one('sparkit.communityworkflowparameters',
		string="Workflow Configuration",
		default=1, track_visibility='onchange')

	# Baseline (Scouting)-> Introductions
	is_oca1_completed = fields.Boolean(string="Baseline Community Assessment Completed",
		track_visibility='onchange',
		compute='check_ocas_completed',
		help="Marked as completed once baseline assessment has been uploaded to the system.")

	# Formal Meeting (Scouting) -> Partnership
	is_community_description_filled = fields.Boolean(string="Community Description Filled",
		compute="check_community_description",
		track_visibility='onchange',
		help="Fill in the community description.")
	has_pm_approved_partnership = fields.Boolean(string="Manager Approved Community For Partnership",
		track_visibility='onchange',
		readonly=True,
		help="The community's manager must approve community partnership. If you are the manager, please click the button that says 'Community Approved for Partnership.'")
		# Activities
	introducing_spark_completed = fields.Boolean(string="Facilitation Activity: Introducing Spark Completed",
		compute='_check_introducing_spark_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Spark Introduction Activity is reported on the visit report form.")
	community_mapping_completed = fields.Boolean(string="Facilitation Activity: Community Mapping Completed",
		compute='_check_community_mapping_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Community Mapping Activity is reported on the visit report form.")

	#Partnership -> Community Building
	partnership_agreement_signed = fields.Boolean(string="Facilitation Activity: Partnership Agreement",
		compute='_check_partnership_agreement_signed',
		track_visibility='onchange',
		store = True,
		help="This is automatically marked as completed when Partnership Agreement Signed activity is reported on the visit report form.")
	is_partnership_hh_requirement_met = fields.Boolean(string="Minimum % of Community Signed Partnership Agreement",
		compute='check_hh_requirement_met',
		track_visibility='onchange',
		help="Did the minimum number of households in the community sign the partnership agreement? This field is located under the 'Important Documents' tab underneath 'Community Detail'.")
		#Activities
	partnership_expectations_completed = fields.Boolean(string="Facilitation Activity: Partnership Expectations",
		compute='_check_partnership_expectations_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Partnership Expectations Activity is reported on the visit report form.")
	planning_group_completed = fields.Boolean(string="Planning Group Household Size Filled In?",
		compute='check_planning_group',
		help="Automatically completed once planning group (under demographics) is filled in on the community profile.")


	# Community Building -> Goal Setting: Goals
	is_cmty_leaders_entered = fields.Boolean(string="Community Contact Information (Leaders) Entered",
		compute='check_community_leaders',
		track_visibility='onchange',
		help="Are there community leaders for the community? The 'Community Leaders' tab is under the community detail.")
	is_office_file_created = fields.Boolean(string="Office File Created",
		track_visibility='onchange',
		help="Did you create a folder in the office to store hard copies of community documents?")
	is_partnerhip_agreement_stored = fields.Boolean(string="Partnership Agreement Stored In Office File",
		track_visibility='onchange',
		help="Did you store a hard copy of the partnership agreement in the office folder?")
	is_partnership_agreement_uploaded = fields.Boolean(string="Partnership Agreement Uploaded",
		compute='check_partnership_agreement_uploaded',
		track_visibility='onchange',
		help="Automatically marked as complete when the partnership agreement is uploaded under 'Important Documents'")
	num_leaders_requirement = fields.Boolean(string="Minimum Number of Leaders Elected",
		compute='check_num_elected_leaders',
		track_visibility='onchange',
		help="Automatically checked when there leaders entered in 'Community Leaders' under 'Community Detail' and the number of leaders is not under the mininum requirement.")
	leaders_gender_requirement = fields.Boolean(string="Minimum Percent of Leaders Are Women",
		compute='check_gender_elected_leaders',
		store=True,
		track_visibility='onchange',
		help="Automatically checks the gender of all community leaders underneath the community profile.")
		# -> Activities
	sms_registration_completed = fields.Boolean(string="SMS Registration Completed",
		track_visibility='onchange',
		help="Please register the community for the SMS system.")
	gender_empowerment_completed = fields.Boolean(string="Facilitation Activity: Gender Empowerment Completed",
		compute='_check_gender_empowerment_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Gender Empowerment Activity is reported on the visit report form.")
	ground_rules_completed = fields.Boolean(string="Facilitation Activity: Ground Rules Completed",
		compute='_check_ground_rules_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Gender Empowerment Activity is reported on the visit report form.")
	strong_leaders_completed = fields.Boolean(string="Facilitation Activity: Qualities of Strong Leaders Completed",
		compute='_check_strong_leaders_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Qualities of Strong Leaders is reported on the visit report form.")
	leadership_election_completed = fields.Boolean(string="Facilitation Activity: Leadership Election",
		compute='_check_leadership_election',
		track_visibility='onchange',
		help="Automatically marked as completed when Leadership Election Activity is reported on the visit report form.")
	vision_statement_completed = fields.Boolean(string="Facilitation Activity: Vision Statement Completed",
		compute='_check_vision_statement_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Vision Statement Activity is reported on the visit report form.")


	# Goal Setting: Goals -> Goal Setting: Pathways
	is_min_goals_brainstormed = fields.Boolean(string="Minimum # of Goals Brainstormed",
		compute='check_goals_ideas',
		track_visibility='onchange',
		help="Was the minimum requirement for the number of goals met? Please fill in 'Goals - Ideas' underneath the 'Projects' tab.")
	is_goals_ideas_not_null = fields.Boolean(string="Goals - Ideas Complete",
		track_visibility='onchange',
		compute='check_goals_ideas',
		help="Please fill in Goals - Ideasunderneath the 'Projects' tab.")
	is_goals_selected_not_null = fields.Boolean(string="Goals - Selected Complete",
		compute='check_goals_selected',
		track_visibility='onchange',
		help="Automatically checked when a description of the goal is filled in under 'Goals - Selected' on the 'Projects' tab.")
	understanding_goals_completed = fields.Boolean(string="Facilitation Activity: Understanding Goals",
		compute='check_understanding_goals_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Understanding Goals is reported on the visit report form.")
	brainstorming_goals_completed = fields.Boolean(string="Facilitation Activity: Brainstorming Goals",
		compute='check_brainstorming_goals_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Brainstorming Goals is reported on the visit report form.")
	consensus_building_completed = fields.Boolean(string="Facilitation Activity: Consensus Building",
		compute='check_consensus_building_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Consensus Building is reported on the visit report form.")
	defining_success_completed = fields.Boolean(string="Facilitation Activity: Defining Success Indicators",
		compute='check_defining_success_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Defining Success Indicators is reported on the visit report form.")
	assessing_past_progress_completed = fields.Boolean(string="Facilitation Activity: Assessing Past Progress",
		compute='check_assessing_past_progress_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Assessing Past Progress is reported on the visit report form.")
	goal_indicators_selected = fields.Boolean(string="Goal Indicators Brainstormed",
		compute='check_goal_indicators_brainstormed',
		track_visibility='onchange',
		help="Automatically marked as completed when the community's three chosen indictors are filled in on the 'Projects' tab.")
	goal_indicator_baselines_gathered = fields.Boolean(string="Goal Indicator Baselines Gathered",
		compute='check_goal_indicator_baselines_gathered',
		track_visibility='onchange',
		help="Automatically marked as completed when the baselines for the community's three chosen indicators are filled in on the 'Projects' tab.")


	# Goal Setting: Pathways -> Implementation Plan
	# hard stops
	is_project_description_not_null = fields.Boolean(string="Project Description Completed",
		compute='check_project_description',
		track_visibility='onchange',
		help="Automatically marked as completed when the 'Pathway - Selected' section on the 'Projects' tab is filled in.")
	pm_approved_goal_setting = fields.Boolean(string="Manager Approved Goal Setting (Pathways, Indicators, Goals)",
		track_visibility='onchange',
		help="Marked as completed when community manager approves the chosen goal, pathways and indicators.")
	is_oca2_completed = fields.Boolean(string="Community Assessment #2 Completed",
		compute='check_ocas_completed', store=True,
		track_visibility='onchange',
		help="Marked as completed when there is a 'Community Assessment' where OCA Number on the form is 2. Community Assessments are under M&E forms.")
	is_min_pathways_brainstormed = fields.Boolean(string="Minimum Number of Pathways Brainstormed?",
		compute='check_pathways_ideas',
		track_visibility='onchange',
		help="Automatically checked when the 'Pathways - Ideas' section underneath the 'Project' tab is at least 5.")
	brainstorming_pathways_completed = fields.Boolean(string="Facilitation Activity: Brainstorming Pathways Completed",
		compute='check_brainstorming_pathways_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Brainstorming Pathways is reported on the visit report form.")
	feasibility_study_completed = fields.Boolean(string="Facilitation Activity: Feasibility Study Completed",
		compute='check_feasibility_study_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Feasibility Study is reported on the visit report form.")
	govt_registration_completed = fields.Boolean(string="Facilitation Activity: Advocacy Training - Government Registration Completed",
		compute='check_govt_registration_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Advocacy Training - Government Registration is reported on the visit report form.")
	introducing_prop_dev = fields.Boolean(string="Facilitation Activity: Introducing Proposal Development",
		compute='check_introducing_prop_dev_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Introducing Proposal Development is reported on the visit report form.")
	devloping_savings_groups = fields.Boolean(string="Facilitation Activity: Developing Savings Groups",
		compute='check_developing_savings_group_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developing Savings Group is reported on the visit report form.")
	banking_training = fields.Boolean(string="Facilitation Activity: Banking Training",
		compute='check_banking_training_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Banking Training is reported on the visit report form.")
	# red flags
	did_ta_recruitment_begin = fields.Boolean(string="TA Recruitment Process Began?",
		track_visibility='onchange',
		help="Check this box if recruitment has begun for a technical advisor")
	did_bank_opening_begin = fields.Boolean(string="Community Began Opening Bank Account?",
		track_visibility='onchange',
		help="Check this box if the community has began the process of opening a bank account for their grant")
	did_government_registration_begin = fields.Boolean(string="Community Began Government Registration Process?",
		track_visibility='onchange',
		help="Check this box if the community has begun to register with the local government")

	# Implementation Plan -> Operational Plan
	is_ta_recruited = fields.Boolean(string="Technical Advisor Recruited/Assigned",
		compute='check_ta_recruited',
		track_visibility='onchange',
		help="Automatically marked as completed when the 'Technical Advisor' field under the 'Projects' tab is filled in with the project's technical advisor.")
	is_ta_workplan_approved = fields.Boolean(string="Technical Advisor Workplan Approved",
		track_visibility='onchange',
		readonly=True,
		help="Has the technical advisor's workplan been approved?")
	is_implementation_action_plan_entered = fields.Boolean(string="Implementation Action Plan Entered Into Proposal",
		track_visibility='onchange')
	developing_implementation_action_plan_completed = fields.Boolean(string="Facilitation Activity: Developing Implementation Action Plan Completed",
		compute='check_developing_implementation_action_plan_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developing Implementation Action Plan is reported on the visit report form.")
	facilitation_training_completed = fields.Boolean(string="Facilitation Activity: Facilitation Training Completed",
		compute='check_facilitation_training_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Facilitation Training is reported on the visit report form.")
	understanding_budgeting_completed = fields.Boolean(string="Facilitation Activity: Understanding Budgeting Completed",
		compute='check_understanding_budgeting_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Understanding Budgeting is reported on the visit report form.")
	developing_implementation_budget_completed = fields.Boolean(string="Facilitation Activity: Developing Implementation Budget Completed",
		compute='check_developing_implementation_budget_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developing Implementation Budget is reported on the visit report form.")
	is_implementation_budget_entered = fields.Boolean(string="Implementation Budget Entered Into Proposal",
		track_visibility='onchange')
	is_ta_trained = fields.Boolean(string="Technical Advisor Trained", track_visibility='onchange')
	cmty_facilitators_identified = fields.Boolean(string="Community Facilitators Identified",
		track_visibility='onchange',
		compute='check_cmty_facilitators_identified')

	#Operational Plan -> Measuring Success
	is_operational_plan_entered = fields.Boolean(string="Operational Plan Entered Into Proposal",
		track_visibility='onchange')
	developing_operational_action_plan_completed = fields.Boolean(string="Facilitation Activity: Developing Operational Action Plan Completed",
		compute='check_developing_operational_action_plan_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developing Operational Action Plan is reported on the visit report form.")
	developing_operational_budget_completed = fields.Boolean(string="Facilitation Activity: Developing Operational Budget Completed",
		compute='check_developing_operational_budget_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developinging Operational Budget is reported on the visit report form.")

	# Measuring Success -> Sustainability Plan
	is_measuring_success_entered = fields.Boolean(string="Measuring Success Entered Into Proposal",
		track_visibility='onchange')
	are_goal_targets_entered = fields.Boolean(string="Goal Indicator Targets Entered into Proposal",
		compute='check_goal_targets_entered',
		track_visibility='onchange',
		help="Automatically marked as completed when indicator targets are filled in on the 'Projects' tab.")
	setting_target_numbers_completed = fields.Boolean(string="Facilitation Activity: Setting Target Numbers Completed",
		compute='check_setting_target_numbers_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Setting Target Numbers is reported on the visit report form.")
	developing_data_collection_plan = fields.Boolean(string="Facilitation Activity: Developing Data Collection Plan Completed",
		compute='check_developing_data_collection_plan_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developing Data Collection Plan is reported on the visit report form.")

	# Proposal Dev: Sustainability Plan -> Proposal Finalization
	is_sustainability_plan_entered = fields.Boolean(string="Sustainability Plan Entered Into Proposal",
		track_visibility='onchange')
	risk_assessment_completed = fields.Boolean(string="Facilitation Activity: Risk Assessment",
		compute='check_risk_assessment_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Risk Assessment Completed is reported on the visit report form.")
	developing_bylaws_completed = fields.Boolean(string="Facilitation Activity: Developing By-Laws",
		compute='check_developing_bylaws_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Developing By-Laws is reported on the visit report form.")
	cmty_engagement_plan_completed = fields.Boolean(string="Facilitation Activity: Community Engagement Plan",
		compute='check_cmty_engagement_plan_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Community Engagement Plan is reported on the visit report form.")
	trnsprncy_acctblty_traning_completed = fields.Boolean(string="Facilitation Activity: Transparency & Accountabiity Training",
		compute='check_trnsprncy_acctblty_traning_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Transparency & Accountability Training is reported on the visit report form.")


	# Proposal Review -> Implementation: Grant Agreement
	is_bank_account_created = fields.Boolean(string="Community Bank Account Open",
		compute="_check_bank_account",
		track_visibility='onchange',
		help="Automatically marked as completed when 'Community Bank Account' is filled in underneath the 'Projects' tab.")
	is_oca3_completed = fields.Boolean(string="Community Assessment #3 Completed",
		track_visibility='onchange',
		compute='check_ocas_completed', store=True,
		help="Automatically marked as completed when a Community Assessment Form where the OCA Number is equal to 3")
	is_budget_created = fields.Boolean(string="Approved Community Budget Entered?",
		compute='_check_budget_created',
		track_visibility='onchange',
		help="Automatically checked when the budget is entered into the community's project.")
	is_project_created = fields.Boolean(string="Project Created and Information Entered?",
		compute='_check_project_created',
		track_visibility='onchange',
		help="Automatically marked as completed when a project form is created for the community.")
	has_pm_approved_proposal = fields.Boolean(string="Manager Approved Proposal Plan",
		track_visibility='onchange',
		readonly=True,
		help="Checked when the manager approves the community's pathway plan.")
	cmty_registered_with_govt = fields.Boolean(string="Community Registered with Local Government and Registration Number Added",
		compute='check_cmty_registered_with_govt',
		track_visibility='onchange',
		help="Automatically marked as completed when the community's government registration number is entered on the 'Community Detail' tab.")

	# Grant Agreement -> Accountability/Transparency
	is_receipt_book_received = fields.Boolean(string="Community Received Receipt Book (in local language)", track_visibility='onchange')
	is_disbursement_book_received = fields.Boolean(string="Community Received Disbursement Book (in local language)", track_visibility='onchange')
	is_cashbook_received = fields.Boolean(string="Community Received Cashbook (in local language)", track_visibility='onchange')
	is_grant_agreement_translated = fields.Boolean(string="Grant Agreement In Local Language", track_visibility='onchange')
	min_pg_signed_agreement = fields.Boolean(string="Minimum Percent of Planning Group Households Signed Grant Agreement",
		track_visibility='onchange',
		compute='check_min_pg_signed_grant_agreement')
	pg_signed_agreement = fields.Boolean(string="Planning Group Signed Grant Agreement",
		track_visibility='onchange',
		compute='check_pg_signed_grant_agreement')
		# Activities
	grant_disbursal_training_completed = fields.Boolean(string="Facilitation Activity: Grant Disbursal Training",
		compute='check_grant_disbursal_training_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Grant Disbursal Training is reported on the visit report form.")
	record_keeping_training_completed = fields.Boolean(string="Facilitation Activity: Record Keeping Training",
		compute='check_record_keeping_training_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Record Keeping Training is reported on the visit report form.")
	sms_training_completed = fields.Boolean(string="Facilitation Activity: SMS Training",
		compute='check_sms_training_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when SMS Training is reported on the visit report form.")
	grant_agreement_signing = fields.Boolean(string="Facilitation Activity: Grant Agreement",
		compute='check_grant_agreement_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Grant Agreement is reported on the visit report form.")

	# Accountability/Transparency -> Leadership
	first_disbursement_completed = fields.Boolean(string="Facilitation Activity: First Disbursement",
		compute='check_first_disbursement_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when First Disbursement is reported on the visit report form.")
	trs_acctb_review_completed = fields.Boolean(string="Facilitation Activity: Transparency & Accountability Review Completed",
		compute='check_trs_acctb_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Transparency & Accountability Review is reported on the visit report form.")
	banking_training_review_completed = fields.Boolean(string="Facilitation Activity: Banking Training Review",
		compute='check_banking_training_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Banking Training Review is reported on the visit report form.")
	followup_disbursement = fields.Boolean(string="Facilitation Activity: Follow-up Disbursement",
		compute='check_followup_disbursement_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Follow-up Disbursement is reported on the visit report form.")
	imp_plan_review_completed = fields.Boolean(string="Facilitation Activity: Implementation Plan Review Completed",
		compute='check_imp_plan_review',
		track_visibility='onchange',
		help="Automatically marked as completed when Implementation Plan Review is reported on the visit report form.")
	risk_mitigation_review_completed = fields.Boolean(string="Facilitation Activity: Risk Mitigation Plan Review",
		compute='check_risk_mitigation_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Risk Mitigation Plan Review is reported on the visit report form.")

	# Leadership Review -> Transition Strategy
	leadership_review_completed = fields.Boolean(string="Facilitation Activity: Leadership Review",
		compute='check_leadership_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Leadership Review is reported on the visit report form.")
	bylaw_review_completed = fields.Boolean(string="Facilitation Activity: By-Law Review",
		compute='check_bylaw_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when By-Law Review is reported on the visit report form.")
	advocacy_report_writing_completed = fields.Boolean(string="Facilitation Activity: Advocacy Training - Report Writing",
		compute='check_advocacy_report_writing_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Advocacy Training - Report Writing is reported on the visit report form.")
	cmty_facilitation_training_completed = fields.Boolean(string="Facilitation Activity: Community Facilitation Training",
		compute='check_cmty_facilitation_training_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Community Facilitation Training is reported on the visit report form.")

	# Transition Strategy -> Post Implementation: Management Support (post_implementation1)
	is_project_quality_approved_ta = fields.Boolean(string="Technical Advisor Approved Project Quality",
		track_visibility='onchange')
	is_imp_action_plan_completed = fields.Boolean(string="Manager Verified All Implementation Activities Completed",
		track_visibility='onchange',
		help="Did the community complete all the activities mentioned on their implementation action plan?")
	is_transition_strategy_completed = fields.Boolean(string="Transition Strategy Completed",
		compute='check_transition_strategy',
		track_visibility='onchange',
		help="Automatically marked as completed when a transition strategy form (under M&E Forms) is completed for the community's project.")
	cmty_facilitation_training = fields.Boolean(string="Community Facilitation Training Completed",
		track_visibility='onchange')
	field_audit_passed = fields.Boolean(string="Field Audit Passed", track_visibility='onchange')
	cmty_report1_submitted = fields.Boolean(string="Community Report Submitted", track_visibility='onchange')
	transition_strategy_activity_completed = fields.Boolean(string="Facilitation Activity: Transition Strategy",
		compute='check_transition_strategy_activity_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Transition Strategy is reported on the visit report form.")

	# Management Support (post_implementation1) -> Future Envisioning (post_implementation2)
	is_oca4_completed = fields.Boolean(string="Community Assessment #4 (Month 1) Completed",
		track_visibility='onchange',
		compute='check_ocas_completed')
	is_oca5_completed = fields.Boolean(string="Community Assesment #5 (Month 6) Completed",
		track_visibility='onchange',
		compute='check_ocas_completed')
	operational_plan_review_completed = fields.Boolean(string="Facilitation Activity: Operational Plan Review",
		compute='check_operational_plan_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Operational Plan Review is reported on the visit report form.")
	risk_mitigation_review2_completed = fields.Boolean(string="Facilitation Activity: Risk Mitigation Plan Review",
		compute='check_risk_mitigation_review2_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Risk Mitigation Plan Review is reported on the visit report form.")
	bylaw_review2_completed = fields.Boolean(string="Facilitation Activity: By-Law Review",
		compute='check_bylaw_review2_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when By-Law Review is reported on the visit report form.")
	leadership_review2_completed = fields.Boolean(string="Facilitation Activity: Leadership Review",
		compute='check_leadership_review2_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Leadership Review is reported on the visit report form.")
	transition_strategy_review2_completed = fields.Boolean(string="Facilitation Activity: Transition Strategy Review",
		compute='check_transition_strategy_review2_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Transition Strategy Review is reported on the visit report form.")

	# Future Envisioning (post_implementation2) -> Graduation (post_implementation3)
	is_oca6_completed = fields.Boolean(string="Community Assessment #6 (Month 12) Completed",
		track_visibility='onchange',
		compute='check_ocas_completed')
	goals_measuring_success_review_completed = fields.Boolean(string="Facilitation Activity: Goal Setting and Measuring Success Review",
		compute='check_goals_measuring_success_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Goal Setting and Measuring Success Review is reported on the visit report form.")
	future_goal_setting_completed = fields.Boolean(string="Facilitation Activity: Future Goal Setting",
		compute='check_future_goal_setting_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Future Goal Setting is reported on the visit report form.")
	advocacy_training_completed = fields.Boolean(string="Facilitation Activity: Advocacy Training",
		compute='check_advocacy_training_comleted',
		track_visibility='onchange',
		help="Automatically marked as completed when Advocacy Training is reported on the visit report form.")
	cmty_facilitator_followup = fields.Boolean(string="Facilitation Activity: Community Facilitation Follow-up",
		compute='check_cmty_facilitator_followup',
		track_visibility='onchange',
		help="Automatically marked as completed when Community Facilitation Follow-up is reported on the visit report form.")
	transition_plan_review = fields.Boolean(string="Facilitation Activity: Transition Plan Review",
		compute='check_transition_plan_review_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Transition Plan Review is reported on the visit report form.")
	cmty_report2_submitted = fields.Boolean(string="Community Progress Report Submitted",
		track_visibility='onchange')

	# Post Implementation 3 -> Graduation
	is_all_mg_disbursed = fields.Boolean(string="All Microgrant Disbursed",
		compute='check_all_mg_disbursed', track_visibility='onchange')
	are_all_receipts_collected = fields.Boolean(string="All Receipts Verified and Collected",
		track_visibility='onchange',
		compute='check_all_receipts_collected')
	cmty_passed_field_audit_pi3 = fields.Boolean(string="Community Passed Field Audit", track_visibility='onchange')
	cmty_report3_submitted = fields.Boolean(string="Community Report #3 Submitted", track_visibility='onchange')
	are_transition_strategy_activities_completed = fields.Boolean(string="Community Completed Transition Strategy Activities",
		track_visibility='onchange')
	is_oca7_completed = fields.Boolean(string="Community Assessment #7 (Month 18) Completed",
		track_visibility='onchange',
		compute='check_ocas_completed')
	is_oca8_completed = fields.Boolean(string="Community Assessment #8 (Month 24) Completed",
		track_visibility='onchange',
		compute='check_ocas_completed')
	exit_agreement_uploaded = fields.Boolean(string="Exit Agreement Uploaded",
		track_visibility='onchange',
		compute='check_exit_agreement_uploaded')
	exit_agreement_signed = fields.Boolean(string="Exit Agreement Signed By Minimum Percent of Planning Group",
		track_visibility='onchange',
		compute='check_exit_agreement_signed')
	graduation_preparation_completed = fields.Boolean(string="Facilitation Activity: Graduation Preparation",
		compute='check_graduation_preparation_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Graduation Preparation is reported on the visit report form.")
	graduation_completed = fields.Boolean(string="Facilitation Activity: Graduation",
		compute='check_graduation_completed',
		track_visibility='onchange',
		help="Automatically marked as completed when Graduation is reported on the visit report form.")


	@api.multi
	@api.depends('cvrf_ids')
	def _get_number_planning_visits(self):
		for r in self:
			if r.cvrf_ids:
				total = 0
				for line in r.cvrf_ids:
					if (line.state == 'approved' and line.visit_type != 'meeting_other' and line.visit_type != 'committee_meeting'):
						total = total + 1
				r.number_planning_visits = total

	@api.multi
	@api.depends('ivrf_ids')
	def _get_number_implementation_visits(self):
		for r in self:
			if r.ivrf_ids:
				total = 0
				for line in r.ivrf_ids:
					if (line.state == 'approved' and line.visit_type != 'meeting_other' and line.visit_type != 'committee_meeting'):
						total = total + 1
				r.number_implementation_visits = total

	@api.multi
	@api.depends('pivrf_ids')
	def _get_number_pi_visits(self):
		for r in self:
			if r.pivrf_ids:
				total = 0
				for line in r.pivrf_ids:
					if (line.state == 'approved' and line.visit_type != 'meeting_other' and line.visit_type != 'committee_meeting'):
						total = total + 1
				r.number_pi_visits = total


	@api.multi
	@api.depends('num_hh_community', 'country_id')
	def _get_num_ppl_community(self):
		for r in self:
			if r.country_id and r.num_hh_community:
				r.num_ppl_community = r.country_id.num_ppl_per_household * r.num_hh_community

	@api.multi
	@api.depends('vrf_ids')
	def check_graduation_preparation_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 160), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 160), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 160), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.graduation_preparation_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_graduation_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 161), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 161), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 161), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.graduation_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_transition_plan_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 154), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 154), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 154), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.transition_plan_review = True

	@api.multi
	@api.depends('vrf_ids')
	def check_cmty_facilitator_followup(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 153), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 153), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 153), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.cmty_facilitator_followup = True

	@api.multi
	@api.depends('vrf_ids')
	def check_advocacy_training_comleted(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 152), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 152), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 152), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.advocacy_training_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_future_goal_setting_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 151), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 151), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 151), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.future_goal_setting_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_goals_measuring_success_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 150), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 150), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 150), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.goals_measuring_success_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_transition_strategy_review2_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 144), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 144), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 144), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.transition_strategy_review2_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_leadership_review2_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 143), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 143), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 143), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.leadership_review2_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_bylaw_review2_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 142), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 142), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 142), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.bylaw_review2_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_risk_mitigation_review2_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 141), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 141), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 141), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.risk_mitigation_review2_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_operational_plan_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 140), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 140), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 140), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.operational_plan_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_transition_strategy_activity_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 130), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 130), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 130), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.transition_strategy_activity_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_cmty_facilitation_training_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 123), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 123), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 123), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.cmty_facilitation_training_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_advocacy_report_writing_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 122), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 122), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 122), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.advocacy_report_writing_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_bylaw_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 121), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 121), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 121), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.bylaw_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_leadership_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 120), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 120), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 120), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.leadership_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_risk_mitigation_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 115), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 115), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 115), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.risk_mitigation_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_imp_plan_review(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 114), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 114), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 114), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.imp_plan_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_followup_disbursement_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 113), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 113), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 113), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.followup_disbursement = True

	@api.multi
	@api.depends('vrf_ids')
	def check_banking_training_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 112), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 112), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 112), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.banking_training_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_trs_acctb_review_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 111), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 111), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 111), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.trs_acctb_review_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_first_disbursement_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 110), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 110), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 110), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.first_disbursement_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_grant_agreement_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 103), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 103), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 103), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.grant_agreement_signing = True

	@api.multi
	@api.depends('vrf_ids')
	def check_sms_training_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 102), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 102), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 102), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.sms_training_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_record_keeping_training_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 101), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 101), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 101), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.record_keeping_training_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_grant_disbursal_training_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 100), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 100), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 100), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.grant_disbursal_training_completed = True

	@api.depends('bank_account')
	def _check_bank_account(self):
		for r in self:
			if r.bank_account:
				r.is_bank_account_created = True

	@api.depends('govt_registration_number')
	def check_cmty_registered_with_govt(self):
		for r in self:
			if r.govt_registration_number:
				r.cmty_registered_with_govt = True

	@api.multi
	@api.depends('vrf_ids')
	def check_trnsprncy_acctblty_traning_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 83), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 83), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 83), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.trnsprncy_acctblty_traning_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_cmty_engagement_plan_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 82), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 82), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 82), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.cmty_engagement_plan_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_developing_bylaws_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 81), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 81), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 81), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.developing_bylaws_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_risk_assessment_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 80), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 80), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 80), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.risk_assessment_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_setting_target_numbers_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 70), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 70), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 70), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.setting_target_numbers_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_developing_data_collection_plan_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 71), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 71), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 71), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.developing_data_collection_plan = True

	@api.multi
	@api.depends('vrf_ids')
	def check_developing_operational_budget_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 61), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 61), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 61), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.developing_operational_budget_completed = True


	@api.multi
	@api.depends('vrf_ids')
	def check_developing_operational_action_plan_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 60), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 60), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 60), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.developing_operational_action_plan_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_developing_implementation_budget_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 53), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 53), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 53), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.developing_implementation_budget_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_understanding_budgeting_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 52), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 52), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 52), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.understanding_budgeting_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_facilitation_training_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 51), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 51), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 51), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.facilitation_training_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_developing_implementation_action_plan_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 50), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 50), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 50), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.developing_implementation_action_plan_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_banking_training_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 45), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 45), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 45), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.banking_training = True

	@api.multi
	@api.depends('vrf_ids')
	def check_developing_savings_group_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 44), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 44), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 44), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.devloping_savings_groups = True

	@api.multi
	@api.depends('vrf_ids')
	def check_introducing_prop_dev_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 43), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 43), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 43), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.introducing_prop_dev = True

	@api.multi
	@api.depends('vrf_ids')
	def check_govt_registration_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 42), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 42), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 42), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.govt_registration_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_feasibility_study_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 41), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 41), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 41), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.feasibility_study_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_brainstorming_pathways_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 40), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 40), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 40), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.brainstorming_pathways_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_understanding_goals_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 30), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 30), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 30), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.understanding_goals_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_brainstorming_goals_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 31), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 31), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 31), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.brainstorming_goals_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_assessing_past_progress_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 34), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 34), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 34), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.assessing_past_progress_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_defining_success_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 33), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 33), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 33), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.defining_success_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def check_consensus_building_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 32), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 32), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 32), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.consensus_building_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_gender_empowerment_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 20), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 20), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 20), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.gender_empowerment_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_ground_rules_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 21), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 21), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 21), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.ground_rules_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_strong_leaders_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 22), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 22), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 22), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.strong_leaders_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_leadership_election(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 23), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 23), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 23), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.leadership_election_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_vision_statement_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 24), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 24), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 24), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.vision_statement_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_partnership_expectations_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 10), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 10), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 10), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.partnership_expectations_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_partnership_agreement_signed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 11), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 11), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 11), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.partnership_agreement_signed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_introducing_spark_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 1), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 1), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 1), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.introducing_spark_completed = True

	@api.multi
	@api.depends('vrf_ids')
	def _check_community_mapping_completed(self):
		for r in self:
			if r.vrf_ids:
				activity1 = r.vrf_ids.search([('activity1_id.number', '=', 3), ('community_number', '=', r.community_number)])
				activity2 = r.vrf_ids.search([('activity2_id.number', '=', 3), ('community_number', '=', r.community_number)])
				activity3 = r.vrf_ids.search([('activity3_id.number', '=', 3), ('community_number', '=', r.community_number)])
				if activity1 or activity2 or activity3:
					r.community_mapping_completed = True

	@api.depends('spark_project_ids')
	def check_all_mg_disbursed(self):
		for r in self:
			if r.spark_project_ids:
				total_left_to_disburse = sum(s.left_to_disburse for s in r.spark_project_ids)
				if total_left_to_disburse == 0:
					r.is_all_mg_disbursed = True

	@api.depends('spark_project_ids')
	def check_all_receipts_collected(self):
		for r in self:
			if r.spark_project_ids:
				total_outstanding_receipts = sum(s.outstanding_receipts for s in r.spark_project_ids)
				if total_outstanding_receipts == 0:
					r.are_all_receipts_collected = True

	@api.depends('indicator1_6month_target', 'indicator1_12months_target',
		'indicator1_18months_target', 'indicator1_2years_target',
		'indicator2_6month_target', 'indicator2_12months_target',
		'indicator2_18months_target', 'indicator2_2years_target',
		'indicator3_6month_target', 'indicator3_12months_target',
		'indicator3_18months_target', 'indicator3_2years_target')
	def check_goal_targets_entered(self):
		for r in self:
			if (r.indicator1_6month_target and
				r.indicator1_12months_target and
				r.indicator1_18months_target and
				r.indicator1_2years_target and
				r.indicator2_6month_target and
				r.indicator2_12months_target and
				r.indicator2_18months_target and
				r.indicator2_2years_target and
				r.indicator3_6month_target and
				r.indicator3_12months_target and
				r.indicator3_18months_target and
				r.indicator3_2years_target):
				r.are_goal_targets_entered = True

	@api.depends('num_hh_in_planning_group')
	def check_planning_group(self):
		for r in self:
			if r.num_hh_in_planning_group > 0:
				r.planning_group_completed = True


	@api.depends('exit_agreement')
	def check_exit_agreement_uploaded(self):
		for r in self:
			if r.exit_agreement:
				r.exit_agreement_uploaded = True

	@api.depends('partnership_agreement')
	def check_partnership_agreement_uploaded(self):
		for r in self:
			if r.partnership_agreement:
				r.is_partnership_agreement_uploaded = True

	@api.one
	@api.depends('phase')
	def _get_phase_name(self):
		for r in self:
			if r.phase:
				r.phase_name = dict(self.fields_get(allfields=['phase'])['phase']['selection'])[self.phase]

	@api.depends('indicator1_baseline', 'indicator2_baseline', 'indicator3_baseline')
	def check_goal_indicator_baselines_gathered(self):
		for r in self:
			if r.indicator1_baseline and r.indicator2_baseline and r.indicator3_baseline:
				r.goal_indicator_baselines_gathered = True

	@api.depends('indicator1', 'indicator2', 'indicator3')
	def check_goal_indicators_brainstormed(self):
		for r in self:
			if r.indicator1 and r.indicator2 and r.indicator3:
				r.goal_indicators_selected = True

	@api.one
	@api.depends('state')
	def _get_state_name(self):
		for r in self:
			if r.state:
				r.state_name = dict(self.fields_get(allfields=['state'])['state']['selection'])[self.state]

	@api.depends('technical_advisor_id')
	def check_ta_recruited(self):
		for r in self:
			if r.technical_advisor_id:
				r.is_ta_recruited = True
			else:
				is_ta_recruited = False

	@api.depends('pathways_ideas')
	def check_pathways_ideas(self):
		for r in self:
			if r.pathways_ideas:
				if r.pathways_ideas >= r.workflow_config_id.min_pathways_brainstormed:
					r.is_min_pathways_brainstormed = True

	@api.multi
	@api.depends('transition_strategy_ids')
	def check_transition_strategy(self):
		for r in self:
			if r.transition_strategy_ids:
				r.is_transition_strategy_completed = True

	@api.multi
	@api.depends('oca_ids')
	def check_ocas_completed(self):
		for r in self:
			for line in r.oca_ids:
				if line.oca_number == "1":
					r.is_oca1_completed = True
				elif line.oca_number == "2":
					r.is_oca2_completed = True
				elif line.oca_number == "3":
					r.is_oca3_completed = True
				elif line.oca_number == "4":
					r.is_oca4_completed = True
				elif line.oca_number == "5":
					r.is_oca5_completed = True
				elif line.oca_number == "6":
					r.is_oca6_completed = True
				elif line.oca_number == "7":
					r.is_oca7_completed = True
				elif line.oca_number == "8":
					r.is_oca8_completed = True

	@api.depends('project_description')
	def check_project_description(self):
		for r in self:
			if r.project_description:
				r.is_project_description_not_null = True

	@api.multi
	@api.depends('spark_project_ids')
	def _check_project_created(self):
		for r in self:
			if r.spark_project_ids:
				r.is_project_created = True

	@api.multi
	def check_pm_approved_goal_setting(self):
		self.pm_approved_goal_setting = True

	@api.multi
	def check_pm_approved_partnership(self):
		self.has_pm_approved_partnership = True

	@api.multi
	def check_pm_approved_proposal(self):
		self.has_pm_approved_proposal = True

	@api.multi
	def check_pm_approved_project_launch(self):
		self.is_imp_action_plan_completed = True

	@api.multi
	def check_pm_approved_ta_workplan(self):
		self.is_ta_workplan_approved = True

	@api.multi
	def check_pm_verified_transition_strategy_complete(self):
		self.are_transition_strategy_activities_completed = True

	@api.multi
	@api.depends('spark_project_ids.budget_line_item_ids')
	def _check_budget_created(self):
		for r in self:
			for line in r.spark_project_ids:
				if line.budget_line_item_ids:
					r.is_budget_created = True

	@api.depends('goals_ideas')
	def check_goals_ideas(self):
		for r in self:
			if r.goals_ideas:
				r.is_goals_ideas_not_null = True
				if r.goals_ideas >= r.workflow_config_id.min_goals_brainstormed:
					r.is_min_goals_brainstormed = True

	@api.depends('goals_selected')
	def check_goals_selected(self):
		for r in self:
			if r.goals_selected:
				r.is_goals_selected_not_null = True

	@api.multi
	@api.depends('community_leader_ids')
	def check_num_elected_leaders(self):
		for r in self:
			if r.community_leader_ids:
				if (len(r.community_leader_ids) >= r.workflow_config_id.communitybldg_min_elected_leaders and
				len(r.community_leader_ids) <= r.workflow_config_id.communitybldg_max_elected_leaders):
					r.num_leaders_requirement = True

	@api.multi
	@api.depends('community_leader_ids', 'workflow_config_id.communtiybldg_min_percent_female')
	def check_gender_elected_leaders(self):
		for r in self:
			if r.community_leader_ids:
				if len(r.community_leader_ids.search([('gender', '=', 'female'), ('community_id.community_number', '=', r.community_number)])) >= (r.workflow_config_id.communtiybldg_min_percent_female * len(r.community_leader_ids)):
					r.leaders_gender_requirement = True

	@api.multi
	@api.depends('community_leader_ids')
	def _compute_number_female_leaders(self):
		for r in self:
			if r.community_leader_ids:
				total = 0
				for line in r.community_leader_ids:
					if line.gender == 'female':
						total = total + 1
				r.number_female_leaders = total


	@api.multi
	@api.depends('community_leader_ids')
	def _compute_total_leaders(self):
		for r in self:
			if r.community_leader_ids:
				r.total_leaders = len(r.community_leader_ids)

	@api.multi
	@api.depends('community_facilitator_ids')
	def check_cmty_facilitators_identified(self):
		for r in self:
			if r.community_facilitator_ids:
				r.cmty_facilitators_identified = True

	@api.multi
	@api.depends('community_leader_ids')
	def check_community_leaders(self):
		for r in self:
			if r.community_leader_ids:
				r.is_cmty_leaders_entered = True

	@api.multi
	@api.depends('number_signed_grant_agreement', 'workflow_config_id')
	def check_min_pg_signed_grant_agreement(self):
		for r in self:
			if r.number_signed_grant_agreement:
				if r.number_signed_grant_agreement >= r.num_hh_in_planning_group * r.workflow_config_id.percent_pg_signed_grantagreement:
					r.min_pg_signed_agreement = True


	@api.multi
	@api.depends('number_signed_grant_agreement')
	def check_pg_signed_grant_agreement(self):
		for r in self:
			if r.number_signed_grant_agreement:
				r.pg_signed_agreement = True

	@api.multi
	@api.depends('number_signed_exit_agreement')
	def check_exit_agreement_signed(self):
		for r in self:
			if r.number_signed_exit_agreement:
				if r.number_signed_exit_agreement >= r.num_hh_in_planning_group * r.workflow_config_id.percent_pg_signed_exitagreement:
					r.exit_agreement_signed = True

	@api.multi
	@api.depends('workflow_config_id', 'num_hh_community')
	def check_hh_requirement_met(self):
		for r in self:
			if r.num_hh_community > 0:
				if r.workflow_config_id.using_hh_breakpoint is True:
					if r.num_hh_community < r.workflow_config_id.partnership_hh_breakpoint:
						if r.workflow_config_id.partnership_hh_lower * r.num_hh_community <= r.number_signed_partnership_agreement:
							r.is_partnership_hh_requirement_met = True
					else:
						if r.workflow_config_id.partnership_hh_upper * r.num_hh_community <= r.number_signed_partnership_agreement:
							r.is_partnership_hh_requirement_met = True
				elif r.workflow_config_id.using_hh_breakpoint is False:
					if r.workflow_config_id.min_percent_hh_partnership * r.num_hh_community <= r.number_signed_partnership_agreement:
						r.is_partnership_hh_requirement_met = True

	@api.depends('description')
	def check_community_description(self):
		for r in self:
			if r.description:
				r.is_community_description_filled = True

	@api.multi
	@api.depends('independent_project_ids')
	def _get_number_ind_projects(self):
		for r in self:
			r.total_independent_projects = len(r.independent_project_ids)

	@api.multi
	@api.depends('savings_group_ids')
	def _get_number_hh_savings_group(self):
		for r in self:
			if r.savings_group_ids:
				r.number_hh_savings_group = sum(s.number_hh for s in r.savings_group_ids)

	@api.multi
	@api.depends('vrf_ids')
	def _get_visit_date(self):
		for r in self:
			if r.vrf_ids:
				vrf_max_date = max(s.visit_date for s in r.vrf_ids)
				vrf_max_id = r.vrf_ids.search([('visit_date', '=', vrf_max_date), ('community_number', '=', r.community_number)], limit=1)
				r.next_visit_date = vrf_max_id.next_visit_date
				r.last_visit_date = vrf_max_id.visit_date
				if r.next_visit_date:
					next_visit_date = datetime.strptime((str(r.next_visit_date)), '%Y-%m-%d').date()
					r.next_visit_date_week = next_visit_date.strftime("%W")

	@api.multi
	@api.depends('vrf_ids')
	def get_grad_metrics(self):
		for r in self:
			if r.vrf_ids:
				ninety_days_ago = datetime.today() - timedelta(days=90)
				vrf_set_ids = r.vrf_ids.search([('visit_date', '>', ninety_days_ago), ('community_number', '=', r.community_number), ('state', '=', 'approved'), ('visit_type', '!=', 'meeting_other'), ('visit_type', '!=', 'committee_meeting') ])
				if vrf_set_ids:
					r.avg_attendance = round(sum(line.attendance_total for line in vrf_set_ids) / len(vrf_set_ids),4)
					r.avg_participation = round(sum(line.speakers_total for line in vrf_set_ids) / len(vrf_set_ids),4)
					if (r.avg_attendance > 0) and (r.num_hh_in_planning_group > 0) and (r.avg_participation > 0):
						r.avg_female_attendance = sum(line.attendance_females for line in vrf_set_ids) / len(vrf_set_ids)
						r.avg_percent_female_attendance = round(r.avg_female_attendance / r.avg_attendance,3)
						r.avg_percent_female_attendance_display = str(r.avg_percent_female_attendance * 100) + "%"						
						r.avg_percent_participation = round(r.avg_participation / r.avg_attendance,3)
						r.avg_percent_participation_display = str(r.avg_percent_participation * 100) + "%"												
						r.avg_percent_female_participation = round((sum(line.speakers_female for line in vrf_set_ids)  / len(vrf_set_ids))/ r.avg_participation,3)
						r.avg_percent_female_participation_display = str(r.avg_percent_female_participation * 100) + "%"																		
						r.avg_percent_pg_participation = round(r.avg_attendance / r.num_hh_in_planning_group,3)
						r.avg_percent_pg_participation_display = str(r.avg_percent_pg_participation * 100) + "%"
					else:
						r.avg_female_attendance = 0
						r.avg_percent_female_attendance = 0
						r.avg_participation = 0
						r.avg_percent_participation = 0
						r.avg_percent_female_participation = 0
						r.avg_percent_pg_participation = 0

	# Think about partners ... do we want them starting from 10,000 or having their
	# own prefix codes?
	# Automatically Generating Next ID when Record is Created
	# First checks to see if the value of country field is equal to:
	# Rwanda = 193, Uganda = 232, Burundi = 25, else
	# Returns to default (ex: 002) without country prefix if matching country not found
	# Then returns sequence paired with country once record is saved

	@api.model
	def create(self, vals):
		if vals.get('country_id')==193:
			if vals:
				vals.update({
					'community_number': self.env['ir.sequence'].next_by_code('scouted.community.rw')
				})
				return super(Community, self).create(vals)
		elif vals.get('country_id')==232:
			if vals:
				vals.update({
					'community_number': self.env['ir.sequence'].next_by_code('scouted.community.ug')
				})
				return super(Community, self).create(vals)
		elif vals.get('country_id')==25:
			if vals:
				vals.update({
					'community_number': self.env['ir.sequence'].next_by_code('scouted.community.bdi')
				})
				return super(Community, self).create(vals)
		else:
			if vals:
				vals.update({
					'community_number': self.env['ir.sequence'].next_by_code('scouted.community.def')
				})
				return super(Community, self).create(vals)

	##Workflow States

	# Workflow Start: Community Identification - Baseline
	@api.multi
	def action_community_identification(self):
		self.phase = 'community_identification'
		self.state = 'community_identification'

	# Baseline - Introductions
	# Sets state from community_identification to introductions
	@api.multi
	def action_introductions(self):
		# First Checks to see if workflow_config_id.is_oca1_completed is True
		# and if is_oca_completed is False
		# If it passes this condition then community can move to next state
		if (self.workflow_config_id.is_oca1_completed is True and
			self.is_oca1_completed is False):
			raise ValidationError("Error: Baseline Community Assessment Must Be Completed!")
		else:
			self.state = 'introductions'

	# Introductions -> Community Building
	# Sets state to partnership, phase to planning, and is_partnered/is_active to true
	@api.multi
	def action_partnership(self):
		# First checks if community Description is filled, because this is always required
		if self.is_community_description_filled is False:
			raise ValidationError("Error: Community Missing Description")
		# Checking to see if PM approval is required per workflow and if it has been entered
		elif self.has_pm_approved_partnership is False:
				raise ValidationError("Error: Manager Must Approve Community For Partnership")
		# If community passes these two conditions then it is partnered:
		else:
			self.state = 'partnership'
			self.phase = 'planning'
			self.is_partnered = True
			self.is_active = True
			# Checks country id to see if it is equal to Rwanda, Burundi or Uganda
			# If equal, the community number if updated using the country-specific sequence
			# If partnership is not one of these three countries, then defaults to a generic sequence
			if self.country_id.id == 193:
				if self.community_number[:2] == "RW":
					self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.rw')
			elif self.country_id.id == 232:
				if self.community_number[:2] == "UG":
					self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.ug')
			elif self.country_id.id == 25:
				if self.community_number[:2] == "BU":
					self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.bdi')
			else:
				self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.def')


	# Partnership -> Community Building
	def action_community_building(self):
		# First checks to see if workflow_config_id.is_partnership_hh_requirement_met is
		# True and is_partnership_hh_requirement_met False.
		# If it passes this condition then community can move to next stage.
		if (self.workflow_config_id.is_partnership_hh_requirement_met is True and
			self.is_partnership_hh_requirement_met is False):
			raise ValidationError("Error: At least %d percent of Households Must Have Signed Partnership Agreement" % (self.workflow_config_id.min_percent_hh_partnership * 100))
		elif self.planning_group_completed is False:
			raise ValidationError("Error: You must enter the number of households in the planning group on the community profile!")
		else:
			self.state = 'community_building'

	# Community Building: Goal setting: Goals
	# Always need to be true: is_office_file_created, is_partnership_agreement_stored,
	#  is_partnership_agreement_uploaded
	# If these conditions are passed, checks to see if fields that are
	# required per workflow are false
	# If the above are passed then self.state = 'goal_setting_goals'
	def action_goal_setting_goals(self):
		if self.is_office_file_created is False:
			raise ValidationError("Error: Community Office File Must Be Created")
		elif self.is_partnerhip_agreement_stored is False:
			raise ValidationError("Error: Partnership Agreement Must Be Stored in Office File!")
		elif self.is_partnership_agreement_uploaded is False:
			raise ValidationError("Error: Partnership Agreement Must Be Uploaded!")
		elif (self.workflow_config_id.is_cmty_leaders_entered is True and
			self.is_cmty_leaders_entered is False):
			raise ValidationError("Error: Community Leaders Must Be Entered")
		elif (self.workflow_config_id.num_leaders_requirement is True and
			self.num_leaders_requirement is False):
			# Checks to see if the project has too many or too little leaders
			if len(self.community_leader_ids) > self.workflow_config_id.communitybldg_max_elected_leaders:
				raise ValidationError("Error: Too Many Project Leaders. The maximum number of leaders a community may have is %d." % self.workflow_config_id.communitybldg_max_elected_leaders)
			elif len(self.community_leader_ids) < self.workflow_config_id.communitybldg_min_elected_leaders:
				raise ValidationError("Error: Too Little Project Leaders. The minimum number of leaders a community may have is %d." % self.workflow_config_id.communitybldg_min_elected_leaders)
		elif (self.workflow_config_id.leaders_gender_requirement is True and
			self.leaders_gender_requirement is False):
			raise ValidationError("Error: At Least %d percent of Leaders Must Be Female!" % (self.workflow_config_id.communtiybldg_min_percent_female * 100))
		elif (self.workflow_config_id.sms_registration_completed is True and
			self.sms_registration_completed is False):
			raise ValidationError("Error: SMS Registration Must Be Completed")
		else:
			self.state = 'goal_setting_goals'

	# Goals -> Goal Setting: Pathways
	def action_goal_setting_pathways(self):
		# All fields here are always required?
		# Older communities minimum goals brainstormed = 0
		if self.is_min_goals_brainstormed is False:
			raise ValidationError("Error: Not Enough Goals - Ideas Brainstormed! The community must brainstorm at least %d goals." % self.workflow_config_id.min_goals_brainstormed)
		elif self.is_goals_ideas_not_null is False:
			raise ValidationError("Error: Goals - Ideas Must Be Filled on Community Profile")
		elif self.is_goals_selected_not_null is False:
			raise ValidationError("Error: Goals - Selected Must Be Filled on Community Profile")
		elif self.goal_indicators_selected is False:
			raise ValidationError("Error: Goal Indicators Must Be Selected and Filled Out On Community Profile")
		elif self.goal_indicator_baselines_gathered is False:
			raise ValidationError("Error: Goal Indicator Baselines Must Be Collected and Filled Out On Community Profile")
		else:
			self.state = 'goal_setting_pathways'

	# Goal Setting: Pathways -> Proposal Development: Implementation Action Plan
	def action_implementation_plan(self):
		# First checks to see required fields are filled in:
		if self.is_min_pathways_brainstormed is False:
			raise ValidationError("Error: Not Enough Pathways - Ideas Brainstormed! The community must brainstorm at least %d pathways." % self.workflow_config_id.min_pathways_brainstormed)
		elif self.is_project_description_not_null is False:
			raise ValidationError("Error: Project Description Must Be Filled on Community Profile")
		# Loops through and checks to see if other fields are required
		# in the workflow and if they are, if they are false
		elif (self.workflow_config_id.is_oca2_completed is True and
			self.is_oca2_completed is False):
			raise ValidationError("Error: OCA2 Must Be Completed!")
		elif (self.workflow_config_id.did_ta_recruitment_begin is True and
			self.did_ta_recruitment_begin is False):
			raise ValidationError("Error: Technical Assistant Recruitment Must Have Begun")
		elif (self.workflow_config_id.did_bank_opening_begin is True and
			self.did_bank_opening_begin is False):
			raise ValidationError("Error: Bank Account Opening Process Must Have Begun")
		elif (self.workflow_config_id.did_government_registration_begin is True and
			self.did_government_registration_begin is False):
			raise ValidationError("Error: Community Must Have Begun Government Registration Process")
		elif (self.workflow_config_id.pm_approved_goal_setting is True and
			self.pm_approved_goal_setting is False):
			raise ValidationError("Error: Community Manager Must Approve Goal Setting Section Before Moving to Proposal Development!")
		# If above conditions are passed, state is set to Implementation Plan
		else:
			self.state = 'implementation_plan'

	# Implementation Plan -> Operational Plan
	def action_operational_plan(self):
		# Always required: is_implementation_action_plan_entered, is_implementation_budget_entered,
		# is_ta_recruited, is_ta_trained, is_ta_workplan_approved
		if self.is_implementation_budget_entered is False:
			raise ValidationError("Error: Implementation Budget Must Be Entered Into Proposal")
		elif self.is_ta_trained is False:
			raise ValidationError("Error: Technical Advisor Must Be Trained")
		elif self.is_ta_recruited is False:
			raise ValidationError("Error: Technical Advisor Must Be Recruited and Assigned to Community")
		elif self.is_ta_workplan_approved is False:
			raise ValidationError("Error: Technical Advisor Workplan Must Be Approved")
		elif self.is_implementation_action_plan_entered is False:
			raise ValidationError("Error: Implementation Action Plan Must Be Entered Into Proposal")
		# Checks to see if community facilitators are required
		elif (self.workflow_config_id.cmty_facilitators_identified is True and
			self.cmty_facilitators_identified is False):
			raise ValidationError("Error: Community Facilitators Must Be Identified")
		else:
			self.state = 'operational_plan'

	# Operational Plan -> Measuring Success
	def action_measuring_success(self):
		if self.is_operational_plan_entered is False:
			raise ValidationError("Error: Operational Action Plan and Budget Must Be Entered Into Proposal")
		else:
			self.state = 'measuring_success'

	# Measuring Success -> Sustainability Plan
	def action_sustainability_plan(self):
		if self.is_measuring_success_entered is False:
			raise ValidationError("Error: Measuring Success Must Be Entered Into Proposal")
		elif self.are_goal_targets_entered is False:
			raise ValidationError("Error: Measuring Success Targest Must Be Entered By Indicators")
		else:
			self.state = 'sustainability_plan'

	# Sustainability Plan -> Proposal Finalization
	def action_proposal_review(self):
		if self.is_sustainability_plan_entered is False:
			raise ValidationError("Error: Sustainability Plan Must Be Entered Into Proposal")
		else:
			self.state = 'proposal_review'
			self.phase = 'planning'

	# Proposal Finalization -> Implementation: Grant Agreement
	def action_grant_agreement(self):
		# Required: budget and project to be Entered
		if self.is_project_created is False:
			raise ValidationError("Error: Community Project Must Be Created")
		elif self.is_budget_created is False:
			raise ValidationError("Error: Community Budget Must Be Entered")
		# Next checks to see if other fields are required per workflow
		elif (self.workflow_config_id.is_bank_account_created is True and
			self.is_bank_account_created is False):
			raise ValidationError("Error: Community Bank Account Must Be Open")
		elif (self.workflow_config_id.has_pm_approved_proposal is True and
			self.has_pm_approved_proposal is False):
			raise ValidationError("Error: Manager Must Approve Community Pathway Plan!")
		elif (self.workflow_config_id.is_oca3_completed is True and
			self.is_oca3_completed is False):
			raise ValidationError("Error: Community Assessment #3 Must Be Completed")
		elif (self.workflow_config_id.cmty_registered_with_govt is True and
			self.cmty_registered_with_govt is False):
			raise ValidationError("Error: Community Must Be Registered with Local Government and Registration Number Must Be Entered")
		else:
			self.state = 'grant_agreement'
			self.phase = 'implementation'


	# Grant Agreement -> Accountability/Transparency (Disbursements Begin)
	def action_first_disbursement(self):
		if (self.workflow_config_id.is_receipt_book_received is True and
			self.is_receipt_book_received is False):
			raise ValidationError("Error: Community Must Have Received Receipt Book")
		elif (self.workflow_config_id.is_disbursement_book_received is True and
			self.is_disbursement_book_received is False):
			raise ValidationError("Error: Community Must Have Received Disbursement Record Book")
		elif (self.workflow_config_id.is_cashbook_received is True and
		 	self.is_cashbook_received is False):
			raise ValidationError("Error: Community Must Have Cashbook")
		elif self.is_grant_agreement_translated is False:
			raise ValidationError("Error: Grant Agreement Must Be Translated in Local Language!")
		elif self.pg_signed_agreement is False:
			raise ValidationError("Error: Planning Group Must Have Signed Grant Agreement")
		elif (self.workflow_config_id.min_pg_signed_agreement is True and
			self.min_pg_signed_agreement is False):
			raise ValidationError("Error: At least %d percent of planning group households must sign grant agreement!" % (self.workflow_config_id.percent_pg_signed_grantagreement * 100))
		else:
			self.state = 'first_disbursement'

	# Imp: A/T (First Disbursement) -> Imp: Leadership
	def action_leadership(self):
		self.state = 'leadership'

	# Imp: Leadership -> Imp: Transition Strategy
	def action_imp_transition_strategy(self):
		self.state = 'imp_transition_strategy'
		self.phase = 'implementation'

	# Imp: Transition Strategy -> Post Implementation 1
	def action_post_implementation1(self):
		if (self.workflow_config_id.is_project_quality_approved_ta is True and
			self.is_project_quality_approved_ta is False):
			raise ValidationError("Error: Technical Advisor Must Approve Project Quality and Launch")
		elif (self.workflow_config_id.is_imp_action_plan_completed is True and
			self.is_imp_action_plan_completed is False):
			raise ValidationError("Error: Completion of Implementation Action Plan Activities Must Be Verified By Manager")
		elif (self.workflow_config_id.is_transition_strategy_completed is True and
			self.is_transition_strategy_completed is False):
			raise ValidationError("Error: Transition Strategy Must Be Completed")
		elif (self.workflow_config_id.cmty_facilitation_training is True and
			self.cmty_facilitation_training is False):
			raise ValidationError("Error: Community Facilitation Training Must Be Completed")
		elif (self.workflow_config_id.field_audit_passed is True and
			self.field_audit_passed is False):
			raise ValidationError("Error: Community Must Have Passed Field Audit")
		elif (self.workflow_config_id.cmty_report1_submitted is True and
			self.cmty_report1_submitted is False):
			raise ValidationError("Error: Community Report Must Have Been Submitted")
		else:
			self.state = 'post_implementation1'
			self.phase = 'post_implementation'
			self.still_meeting = True
			self.project_sustaining = True


	def action_post_implementation2(self):
		if (self.workflow_config_id.is_oca4_completed is True and
			self.is_oca4_completed is False):
			raise ValidationError("Error: Community Assessment #4 (Month 1) Must Be Completed")
		elif (self.workflow_config_id.is_oca5_completed is True and
			self.is_oca5_completed is False):
			raise ValidationError("Error: Community Assessment #5 (Month 6) Must Be Completed")
		else:
			self.state = 'post_implementation2'

	def action_post_implementation3(self):
		if (self.workflow_config_id.is_oca6_completed is True and
			self.is_oca6_completed is False):
			raise ValidationError("Error: Community Assessment #6 (Month 12) Must Be Completed")
		elif (self.workflow_config_id.cmty_report2_submitted is True and
			self.cmty_report2_submitted is False):
			raise ValidationError("Error: Community Report Must Be Submitted")
		self.state = 'post_implementation3'

	def action_graduation(self):
		if (self.workflow_config_id.is_oca7_completed is True and
			self.is_oca7_completed is False):
			raise ValidationError("Error: Community Assessment #7 Must Be Completed")
		elif (self.workflow_config_id.cmty_passed_field_audit_pi3 is True and
			self.cmty_passed_field_audit_pi3 is False):
			raise ValidationError("Error: Community Must Have Passed Field Audit")
		elif self.are_transition_strategy_activities_completed is False:
			raise ValidationError("Error: Manager Must Approve All Transition Strategy Activities Completed")
		elif self.is_all_mg_disbursed is False:
			raise ValidationError("Error: All Remaining MicroGrant Balance Must Be Disbursed")
		elif self.are_all_receipts_collected is False:
			raise ValidationError("Error: All Receipts Must Be Collected")
		elif (self.workflow_config_id.cmty_report3_submitted is True and
			self.cmty_report3_submitted is False):
			raise ValidationError("Error: Community Must Submit Progress Report")
		elif self.number_signed_exit_agreement == 0:
			raise ValidationError("Error: Exit Agreement Must Be Signed!")
		elif (self.workflow_config_id.exit_agreement_signed is True and
			self.exit_agreement_signed is False):
			raise ValidationError("Error: Exit Agreement Must Be Signed by Minimum Percent of Planning Group")
		elif (self.workflow_config_id.exit_agreement_uploaded is True and
			self.exit_agreement_uploaded is False):
			raise ValidationError("Error: Exit Agreement Must Be Uploaded")
		elif (self.workflow_config_id.is_oca8_completed is True and
			self.is_oca8_completed is False):
			raise ValidationError("Error: Community Assessment #8 Must Be Completed")
		else:
			self.is_active = False
			self.state = 'graduated'
			self.phase = 'graduated'

	#---------------------------------------------------
	#                 Constraints                      |
	#---------------------------------------------------

	_sql_constraints = [
		#Unique Community Name
		('name_unique',
    	'UNIQUE(name)',
    	"The community name must be unique"),
    ]



	#---------------------------------------------------
	#      Special Cases Configuration Class          |
	#---------------------------------------------------

class SpecialCases(models.Model):
	_name = 'sparkit.specialcases'

	name = fields.Char(string="Special Case", required=True)
	community_ids = fields.Many2one('sparkit.community', string="Communities")
	