# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError, Warning

# TODO: Automatic Important Dates
# TODO: Think about codes for partner organizations
# TODO: Think about groups!...

class Community(models.Model):
	_name = 'sparkit.community'
	_inherit = 'mail.thread'

	#Basic Information
	name = fields.Char(string="Community Name", required=True)
	description = fields.Text(string="Community Description")
	community_number = fields.Char(string="Community Number", readonly=True)
	scouted_by_id = fields.Many2one('res.users', default=lambda self: self.env.user)
	is_partnered = fields.Boolean(string="Partnered?", default=False)
	facilitator_id = fields.Many2one('res.users', string="Facilitator", default=lambda self: self.env.user)
	program_manager_id = fields.Many2one('res.users', string="Program Manager")
	is_active = fields.Boolean(string="Active?")

	#Workflow States
	phase = fields.Selection([
		('community_identification', 'Community Identification'),
		('planning', 'Planning'),
		('implementation', 'Implementation'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated')
		])

	#Planning Steps
	state = fields.Selection([
		('community_identification', 'Community Identification'),
		('partnership', 'Partnership'),
		('community_building', 'Community Building'),
		('goal_setting_goals', 'Goal Setting: Goals'),
		('goal_setting_objectives', 'Goal Setting: Objectives'),
		('goal_setting_pathways', 'Goal Setting: Pathways'),
		('measuring_success', 'Proposal Development: Measuring Success'),
		('implementation_action_plan', 'Proposal Development: Implementation Action Plan'),
		('implementation_budget', 'Proposal Development: Implementation Budget'),
		('operational_action_plan', 'Proposal Development: Operational Action Plan'),
		('operational_budget', 'Proposal Development: Operational Budget'),
		('sustainability_plan', 'Proposal Development: Sustainability Plan'),
		('transition_strategy', 'Proposal Development: Transition Strategy'),
		('proposal_review', 'Proposal Development: Proposal Review'),
		('grant_agreement', 'Implementation: Grant Agreement & Financial Management'),
		('first_disbursement', 'Implementation: First Dibursement, Accountability & Transparency'),
		('project_management', 'Implementation: Project Management'),
		('leadership', 'Implementation: Leadership'),
		('imp_transition_strategy', 'Implementation: Transition Strategy'),
		('post_implementation', 'Post Implementation'),
		('graduated', 'Graduated'),
		('partnership_canacelled', 'Partnership Cancelled')
	], string="Step")

	#Community Detail
	facilitation_language = fields.Char(string="Facilitation Language")
	is_using_translator = fields.Boolean(string="Using Translator?")
	translator_id = fields.Many2one('res.partner', string="Translator")
	meeting_day = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'),
		('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')],
		select=True, string="Meeting Day",
		help="Please select the day you meet the community for facilitation meetings.")

	#dates
	date_scouted=fields.Date(string="Date Scouted",
		help="Please enter the date the community was scouted")
	partnershp_date = fields.Date(string="Partnership Date")
	implementation_start_date = fields.Date(string="Implementation Start Date")
	post_implementation_start_date = fields.Date(string="Post Implementation Start Date")
	graduation_date = fields.Date(string="Graduation Date")

	#Demographics
	num_hh_community = fields.Integer(string="Number of Households")
	num_ppl_community = fields.Integer(string="Number of People")
	num_households_at_partnership = fields.Integer(string="Number of Households at Partnership",
		help="Please enter the number of households that signed the partnership agreement.")
	num_ppl_at_partnership = fields.Integer(string="Number of People at Partnership")
	num_hh_in_planning_group = fields.Integer(string="Number of Households in Planning Group")
	num_ppl_in_planning_group = fields.Integer(string="Number of People in Planning Group")

	#Location Information
	country_id = fields.Many2one('res.country', string="Country", required=True)
	country_onchange = fields.Many2one('res.country',
		compute="_country_onchange", store=True, readonly=False)
	cell = fields.Char(string="Cell")
	district = fields.Char(string="District")
	village = fields.Char(string="Village")
	province = fields.Char(string="Province")
	sector = fields.Char(string="Sector")
	sub_county = fields.Char(string="Sub County")
	directions_to_community = fields.Text(string="Directions to Community")
	community_gps_coordinates = fields.Char(string="Communiy Center GPS Coordinates")
	bodamoto_drivers = fields.Many2many('res.partner', string="Boda/Moto Drivers")

	#Location - Vulnerability Information
	clean_water_gps_coordinates = fields.Char("GPS Coordinates - Nearest Clean Water Source")
	health_center_gps_coordinates = fields.Char("GPS Coordinates - Nearest Health Center")
	school_gps_coordinates = fields.Char("GPS Coordinates - Nearest School")
	nearest_town_gps_coordinates = fields.Char("GPS Coordinates - Nearest Town")

	nearest_health_center_details = fields.Text("Nearest Health Center Details")
	nearest_school_details = fields.Text("Nearest School Details")
	nearest_town_details = fields.Text("Nearest Town Details")
	nearest_clean_water_details = fields.Text("Nearest Water Access Point Details")

	#Technical Advisor
	technical_advisor_id = fields.Many2one('res.partner', string="Technical Advisor")

	#Project Detail
	goals_ideas = fields.Integer(string="Goals - Ideas",
		help="Please enter the number of ideas the community brainstormed for their goal.")
	goals_selected = fields.Text(string="Goals - Selected",
		help="Please describe the community's chosen goal in their own words.")
	objectives_ideas = fields.Integer(string="Objectives - Ideas",
		help="Please enter the number of ideas the community brainstormed for their objective.")
	objectives_selected = fields.Text(string="Objectives - Selected",
		help="Please describe the community's chosen objective in their own words.")
	pathways_ideas = fields.Integer(string="Pathways - Ideas",
		help="Please enter the number of ideas the community brainstormed for their pathway.")
	project_description = fields.Text(string="Please describe the community's chosen project in their own words.")


	#Leaders
	spark_leader_ids = fields.Many2many('res.partner')
	community_leader_ids = fields.Many2many('res.partner')

	#VRF Forms
	cvrf_ids = fields.One2many('sparkit.cvrf', 'community_id', string="CVRFs")
	ivrf_ids = fields.One2many('sparkit.ivrf', 'community_id', string="IVRFs")
	pivrf_ids = fields.One2many('sparkit.pivrf', 'community_id', string="PIVRFs")

	#Community Project
	spark_project_ids = fields.One2many('sparkit.sparkproject', 'community_id', string="Grant Project")
	project_category_id = fields.Many2one(related='spark_project_ids.category_id')
	project_subcategory_id = fields.Many2one(related='spark_project_ids.subcategory_id')
	project_support_initiative_ids = fields.One2many('sparkit.projectsupportinitiative', 'community_id')

	#Last Visit Date Calculations
	last_visit_date = fields.Date(string="Last Visit Date", compute='_get_last_visit_date')
	cvrf_max_id = fields.Many2one('sparkit.cvrf', compute='_get_max_cvrf_id')
	ivrf_max_id = fields.Many2one('sparkit.ivrf', compute='_get_max_ivrf_id')
	pivrf_max_id = fields.Many2one('sparkit.pivrf', compute='_get_max_pivrf_id')
	phase_id = fields.Many2one(related='step_id.phase_id', string="Phase", readonly=True)
	step_id = fields.Many2one('sparkit.fcapstep', string="Step", compute='_get_step', readonly=True)
	next_visit_date = fields.Date(string="Next Visit Date", compute='_get_next_visit_date')


	#Ind Projects
	independent_project_ids = fields.One2many('sparkit.independentproject',
		'community_id', string="Independent Projects")
	independent_project_update_ids = fields.One2many('sparkit.independentprojectupdate', 'community_id')
	independent_project_total = fields.Integer(compute='_get_number_ind_projects')

	#Independent Meetings
	independent_meeting_ids = fields.One2many('sparkit.independentmeeting', 'community_id', string="Independent Meetings")

	#Savings Groups
	savings_group_ids = fields.One2many('sparkit.savingsgroup', 'community_id',
		string="Savings Groups")
	savings_group_update_ids = fields.One2many('sparkit.savingsgroupupdate', 'community_id')

	#OCAs
	oca_ids = fields.One2many('sparkit.oca', 'community_id', string="OCAs")

	#Pillar Assessments
	pillar_assessment_ids = fields.One2many('sparkit.pillarassessment', 'community_id', string="Pillar Assessments")

	#Transition Strategy
	transition_strategy_ids = fields.One2many('sparkit.transitionstrategy', 'community_id', string="Transition Strategy")

	#Scouting Form
	scouting_form_ids = fields.One2many('sparkit.scoutingform', 'community_id', string="Scouting Form")

	#Partnerships
	partnership_ids = fields.One2many('sparkit.partnership', 'community_id', string="Partnerships")
	partnership_update_ids = fields.One2many(related='partnership_ids.partnership_update_ids')

	#Pilots
	pilot_ids = fields.Many2many('sparkit.pilot', string="Pilots")
	pilot_update_ids = fields.One2many('sparkit.pilotupdate', 'community_id')

	#------Workflow Fields----#
	#workflow configuration
	workflow_config_id = fields.Many2one('sparkit.communityworkflowparameters', string="Workflow Configuration",
		default=1)

	# Formal Meeting (Scouting) -> Partnership
	is_community_description = fields.Boolean(string="Community Description Filled?",
			compute="check_community_description")
	is_oca0_completed = fields.Boolean(string="OCA - Scouting Complete", compute='check_ocas_completed', store=True)

	#Partnership -> Community Building
	is_partnership_agreement_signed = fields.Boolean(string="Partnership Agreement Signed?")
	is_partnership_hh_requirement_met = fields.Boolean(string="Minimum number of Households Signed Partnership Agreement?",
		compute='check_hh_requirement_met')

	# Community Building -> Goal Setting: Goals
	is_oca1_completed = fields.Boolean(string="OCA #1 Completed", compute='check_ocas_completed', store=True)
	is_cmty_leaders_entered = fields.Boolean(string="Community Contact Information (Leaders) Entered?",
		compute='check_community_leaders')
	is_office_file_created = fields.Boolean(string="Office File Created?")
	is_partnerhip_agreement_stored = fields.Boolean(string="Is Partnership Agreement Stored?")
	is_partnership_agreement_uploaded = fields.Boolean(string="Is Partnership Agreement Uploaded?")
	is_spark_leaders_requirement = fields.Boolean(string="# Elected Leaders Meets Requirements", compute='check_elected_leaders')

	# Goal Setting: Goals -> Goal Setting: Objectives
	is_pm_approved_goals = fields.Boolean(string="PM Approved Goals?")
	is_min_goals_brainstormed = fields.Boolean(string="Minimum Goals Brainstormed?", compute='check_goals_ideas')
	is_goals_ideas_not_null = fields.Boolean(string="Goals - Ideas Complete", compute='check_goals_ideas')
	is_goals_selected_not_null = fields.Boolean(string="Goals - Selected Complete", compute='check_goals_selected')

	#Goal Setting: Objectives -> Goal Setting: Pathways
	is_objectives_ideas_not_null = fields.Boolean(string="Objectives - Ideas Commplete",
		compute='check_objectives_ideas')
	is_objectives_selected_not_null = fields.Boolean(string="Objectives - Selected Complete",
		compute='check_objectives_selected')
	is_pm_approved_objectives = fields.Boolean(string="PM Approved Objectives?")

	# Goal Setting: Pathways -> Proposal Development: Measuring Success
	is_project_description_not_null = fields.Boolean(string="Project Description Completed",
		compute='check_project_description')
	is_pm_approved_pathways = fields.Boolean(string="PM Approved Pathway?")
	is_oca2_completed = fields.Boolean(string="OCA #2 Completed?", compute='check_ocas_completed', store=True)
	is_min_pathways_brainstormed = fields.Boolean(string="Minimum Number of Pathways Brainstormed?",
		compute='check_pathways_ideas')

	# Proposal Development: Measuring Success -> Proposal Development: Implementation Action Plan
	is_pm_approved_goals_complete = fields.Boolean(string="PM Approved Goals Section",
		help="Is there a logical link between goals/objectives/pathways section?")

	# Proposal Development: Implementation Action Plan -> Proposal Development: Implementation Budget
	is_microgrant_amount_approved = fields.Boolean(string="Regional Team Approved Grant Size",
		help="Did the CD Sign off?")
	is_ta_workplan_approved = fields.Boolean(string="Technical Advisor Workplan Approved")
	is_ta_recruited = fields.Boolean(string="Technical Advisor Recruited", compute='check_ta_recruited')
	is_measuring_success_approved = fields.Boolean(string="PM Approved Measuring Success")
	is_bank_detail_added = fields.Boolean(string="Bank/Payment Details Added")

	# Proposal Development: Implementation Budget -> Operational Action Plan
	is_implementation_action_plan_approved = fields.Boolean(string="PM Approved Implementation Action Plan")

	# Proposal Dev: Operational Action Plan -> Operational Budget
	is_implementation_budget_approved = fields.Boolean(string="PM Approved Implementation Budget",
		help="Does the budget have contigency funds?")

	# Proposal Dev: Operational Budget -> Sustainability Plan
	is_operational_action_plan_approved = fields.Boolean(string="PM Approved Operational Action Plan")

	# Proposal Dev: Sustainability Plan -> Transition Strategy
	is_operational_budget_approved = fields.Boolean(string="PM Approved Operational Budget?",
		help="Is the budget balanced with a verified source of income? Do the operational action plan/budget link?")

	# Proposal Dev: Transition Strategy -> Proposal Review
	is_sustainability_plan_approved = fields.Boolean(string="PM Approved Sustainability Plan?",
		help="Is the community engagement plan linked to the bylaws and sustainability plan? Are there tangible reasons for monthly meetings? Did the community have a clear response for risk factors?")
	are_bylaws_acknowledged = fields.Boolean(string="By-Laws Acknowleged by Community",
		help="Were the by-laws acknowledged by at least 755 of the planning group?")

	# Proposal Review -> Implementation: Grant Agreemnet + Financial Management
	is_bank_account_open = fields.Boolean(string="Community Bank Account Open")
	is_proposal_approved_by_ta = fields.Boolean(string="Technical Advisor Approved Project Proposal")
	is_proposal_approved_by_team = fields.Boolean(string="PM/Team Approved Proposal")
	is_oca3_completed = fields.Boolean(string="OCA3 Completed", compute='check_ocas_completed', store=True)

	# Grant Agreement -> First Disbursement
	is_receipt_book_received = fields.Boolean(string="Community Received Receipt Book")
	is_disbursement_book_received = fields.Boolean(string="Community Received Disbursement Book")
	is_grant_agreement_translated = fields.Boolean(string="Grant Agreement In Local Language")
	pg_signed_agreement = fields.Boolean(string="Did at least 60percent of PG sign grant agreement?")

	# First Disbursement -> Project Management and (then Leadership)
	is_microgrant_disbursed = fields.Boolean(string="MicroGrant Disbursed")
	is_microgrant_confirmed = fields.Boolean(string="MicroGrant Confirmation Received")

	# Transition Strategy -> PI
	is_launch_approved_ta = fields.Boolean(string="Technical Advisor Approved Launch")
	is_capacity_verified = fields.Boolean(string="PM Visited to Verify Capacity",
		help="Did the TA visit to verify the community's capacity in banking and record keeping?")
	is_imp_action_plan_completed = fields.Boolean(string="PM Verified All Implementation Activities Completed",
		help="Did the community complete all the activities mentioned on their implementation action plan?")
	is_ta_visits_verified = fields.Boolean(string="All Scheduled TA Visits Took Place")
	is_transition_strategy_completed = fields.Boolean(string="Transition Strategy Completed")

	# PI -> Graduation
	is_all_mg_disbursed = fields.Boolean(string="All MicroGrant Disbursed")
	are_all_receipts_collected = fields.Boolean(string="All Receipts Verified and Collected")
	all_ta_trainings_occurred = fields.Boolean(string="PM Verified All TA Trainings Occurred")
	all_pillar_trainings_occured = fields.Boolean(string="PM Verified All Pillar Trainings Occurred")
	did_community_meet_pillars = fields.Boolean(string="Community Has Met Pillar Minimums")
	is_exit_agreement_signed = fields.Boolean(string="Exit Agreement Signed")
	did_community_report_progress = fields.Boolean(string="Community Reported on Progress Towards Communal Goal")
	are_next_steps_established = fields.Boolean(string="Community Established Next Steps Towards Communal Goal")
	are_transition_strategy_activities_completed = fields.Boolean(string="Community Completed Transition Strategy Activities")

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
	@api.depends('oca_ids')
	def check_ocas_completed(self):
		for r in self:
			if r.oca_ids:
				oca0_ids = r.oca_ids.search([('community_id', '=', self.id), ('oca_number', '=', 0)])
				oca1_ids = r.oca_ids.search([('community_id', '=', self.id), ('oca_number', '=', 1)])
				oca2_ids = r.oca_ids.search([('community_id', '=', self.id), ('oca_number', '=', 2)])
				oca3_ids = r.oca_ids.search([('community_id', '=', self.id), ('oca_number', '=', 3)])
				if oca3_ids:
					r.is_oca3_completed = True
				if oca2_ids:
					r.is_oca2_completed = True
				if oca1_ids:
					r.is_oca1_completed = True
				if oca0_ids:
					r.is_oca0_completed = True

	@api.depends('project_description')
	def check_project_description(self):
		for r in self:
			if r.project_description:
				r.is_project_description_not_null = True

	@api.depends('objectives_ideas')
	def check_objectives_ideas(self):
		for r in self:
			if r.objectives_ideas:
				r.is_objectives_ideas_not_null = True

	@api.depends('objectives_selected')
	def check_objectives_selected(self):
		for r in self:
			if r.objectives_selected:
				r.is_objectives_selected_not_null = True


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
	@api.depends('spark_leader_ids')
	def check_elected_leaders(self):
		for r in self:
			if r.spark_leader_ids:
				if len(r.spark_leader_ids) >= r.workflow_config_id.communitybldg_min_elected_leaders and len(r.spark_leader_ids) <= r.workflow_config_id.communitybldg_max_elected_leaders:
					r.is_spark_leaders_requirement = True

	@api.multi
	@api.depends('community_leader_ids')
	def check_community_leaders(self):
		for r in self:
			if r.community_leader_ids:
				r.is_cmty_leaders_entered = True

	@api.multi
	@api.depends('num_households_at_partnership', 'num_hh_community')
	def check_hh_requirement_met(self):
		for r in self:
			if r.num_hh_community > 0:
				if r.num_hh_community < r.workflow_config_id.partnership_hh_breakpoint:
					if r.workflow_config_id.partnership_hh_lower * r.num_hh_community <= r.num_households_at_partnership:
						r.is_partnership_hh_requirement_met = True
				else:
					if r.workflow_config_id.partnership_hh_upper * r.num_hh_community <= r.num_households_at_partnership:
						r.is_partnership_hh_requirement_met = True

	@api.depends('description')
	def check_community_description(self):
		if self.description:
			self.is_community_description = True

	@api.multi
	def _get_number_ind_projects(self):
		for r in self:
			r.independent_project_total = len(r.independent_project_ids)

	@api.multi
	def _get_step(self):
		for r in self:
			if r.pivrf_max_id:
				r.step_id = r.pivrf_max_id.step_id
			elif r.ivrf_max_id:
				r.step_id = r.ivrf_max_id.step_id
			elif r.cvrf_max_id:
				r.step_id = r.cvrf_max_id.step_id

	@api.multi
	def _get_next_visit_date(self):
		for r in self:
			if r.pivrf_max_id:
				r.next_visit_date = r.pivrf_max_id.next_visit_date
			elif r.ivrf_max_id:
				r.next_visit_date = r.ivrf_max_id.next_visit_date
			elif r.cvrf_max_id:
				r.next_visit_date = r.cvrf_max_id.next_visit_date


	@api.multi
	def _get_last_visit_date(self):
		for r in self:
			if r.pivrf_max_id:
				r.last_visit_date = r.pivrf_max_id.visit_date
			elif r.ivrf_max_id:
				r.last_visit_date = r.ivrf_max_id.visit_date
			elif r.cvrf_max_id:
				r.last_visit_date = r.cvrf_max_id.visit_date

	@api.multi
	def _get_max_cvrf_id(self):
		for r in self:
			if r.cvrf_ids:
				cvrf_max_date = max(s.visit_date for s in r.cvrf_ids)
				r.cvrf_max_id = r.cvrf_ids.search([('visit_date', '=', cvrf_max_date), ('community_number', '=', r.community_number)], limit=1)

	@api.multi
	def _get_max_ivrf_id(self):
		for r in self:
			if r.ivrf_ids:
				ivrf_max_date = max(s.visit_date for s in r.ivrf_ids)
				r.ivrf_max_id = r.ivrf_ids.search([('visit_date', '=', ivrf_max_date), ('community_number', '=', r.community_number)], limit=1)

	@api.multi
	def _get_max_pivrf_id(self):
		for r in self:
			if r.pivrf_ids:
				pivrf_max_date = max(s.visit_date for s in r.pivrf_ids)
				r.pivrf_max_id = r.pivrf_ids.search([('visit_date', '=', pivrf_max_date), ('community_number', '=', r.community_number)], limit=1)

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
	@api.multi
	def action_community_identification(self):
		self.phase = 'community_identification'
		self.state = 'community_identification'

	@api.multi
	def action_partnership(self):
		# Sets state to planning and is_partnered to true
		if (self.is_community_description is True and
			self.is_oca0_completed is True):
			self.state = 'partnership'
			self.phase = 'planning'
			self.is_partnered = True
			self.is_active = True
			# Checks country id to see if it is equal to Rwanda, Burundi or Uganda
			# If equal, the community number if updated using the country-specific sequence
			# If partnership is not one of these three countries, then defaults to a generic sequence
			if self.country_id.id == 193:
				self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.rw')
			elif self.country_id.id == 232:
				self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.ug')
			elif self.country_id.id == 25:
				self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.bdi')
			else:
				self.community_number = self.env['ir.sequence'].next_by_code('partnered.community.def')
		elif self.is_community_description is False:
			raise ValidationError("Error: Community Missing Description")
		elif self.is_oca0_completed is False:
			raise ValidationError("Error: OCAs at Scouting Must Be Completd!")

	# Partnership -> Community Building
	def action_community_building(self):
		if self.is_partnership_agreement_signed is True and self.is_partnership_hh_requirement_met is True:
			self.state = 'community_building'
		elif self.is_partnership_agreement_signed is False:
			raise ValidationError("Error: Partnership Agreement Must Be Signed")
		elif self.is_partnership_hh_requirement_met is False:
			raise ValidationError("Error: Minimum Number of Households Must Have Signed Partnership Agreement")

	def action_goal_setting_goals(self):
		if (self.is_oca1_completed is True and self.is_cmty_leaders_entered is True
			and self.is_office_file_created is True
			and self.is_partnerhip_agreement_stored is True
			and self.is_partnership_agreement_uploaded is True
			and self.is_spark_leaders_requirement is True):
			self.state = 'goal_setting_goals'
		elif self.is_oca1_completed is False:
			raise ValidationError("Error: OCA1 Must Be Completed")
		elif self.is_cmty_leaders_entered is False:
			raise ValidationError("Error: Community Leaders Must Be Entered")
		elif self.is_office_file_created is False:
			raise ValidationError("Error: Community Office File Must Be Created")
		elif self.is_partnerhip_agreement_stored is False:
			raise ValidationError("Error: Partnership Agreement Must Be Stored in Office File!")
		elif self.is_partnership_agreement_uploaded is False:
			raise ValidationError("Error: Partnership Agreement Must Be Uploaded!")
		elif self.is_spark_leaders_requirement is False:
			if len(self.spark_leader_ids) > self.workflow_config_id.communitybldg_max_elected_leaders:
				raise ValidationError("Error: Too Many Project Leaders")
			elif len(self.spark_leader_ids) < self.workflow_config_id.communitybldg_min_elected_leaders:
				raise ValidationError("Error: Too Little Project Leaders")

	def action_goal_setting_objectives(self):
		if (self.is_pm_approved_goals is True and
			self.is_min_goals_brainstormed is True and
			self.is_goals_ideas_not_null is True and
			self.is_goals_selected_not_null is True):
			self.state = 'goal_setting_objectives'
		elif self.is_goals_ideas_not_null is False:
			raise ValidationError("Error: Goals - Ideas Must Be Filled on Community Profile")
		elif self.is_min_goals_brainstormed is False:
			raise ValidationError("Error: Not Enough Goals - Ideas Brainstormed!")
		elif self.is_goals_selected_not_null is False:
			raise ValidationError("Error: Goals - Selected Must Be Filled on Community Profile")
		elif self.is_pm_approved_goals is False:
			raise ValidationError("Error: Community Program Manager Must Approve Goals Section!")

	def action_goal_setting_pathways(self):
		if (self.is_objectives_ideas_not_null is True and
			self.is_objectives_selected_not_null is True and
			self.is_pm_approved_objectives is True):
			self.state = 'goal_setting_pathways'
		elif self.is_objectives_ideas_not_null is False:
			raise ValidationError("Error: Objectives - Ideas Must Be Filled on Community Profile")
		elif self.is_objectives_selected_not_null is False:
			raise ValidationError("Error: Objectives - Selected Must Be Filled on Community Profile")
		elif self.is_pm_approved_objectives is False:
			raise ValidationError("Error: Community Program Manager Must Approve Objectives Section!")


	def action_measuring_success(self):
		if (self.is_project_description_not_null is True and
			self.is_pm_approved_pathways is True and
			self.is_oca2_completed is True and
			self.is_min_pathways_brainstormed is True):
			self.state = 'measuring_success'
		elif self.is_min_pathways_brainstormed is False:
			raise ValidationError("Error: Not Enough Pathways - Ideas Brainstormed!")
		elif self.is_project_description_not_null is False:
			raise ValidationError("Error: Project Description Must Be Filled on Community Profile")
		elif self.is_pm_approved_pathways is False:
			raise ValidationError("Error: Community Program Manager Must Approve Pathways Section!")
		elif self.is_oca2_completed is False:
			raise ValidationError("Error: OCA2 Must Be Completed!")

	def action_implementation_action_plan(self):
		if self.is_pm_approved_goals_complete is True:
			self.state = 'implementation_action_plan'
		elif self.is_pm_approved_goals_complete is False:
			raise ValidationError("Error: Program Manager Must Approve Community Goals, Objectives and Pathways")

	def action_implementation_budget(self):
		if (self.is_ta_workplan_approved is True and
			self.is_microgrant_amount_approved is True and
			self.is_ta_recruited is True and
			self.is_measuring_success_approved is True and
			self.is_bank_detail_added is True):
			self.state = 'implementation_budget'
		elif self.is_ta_recruited is False:
			raise ValidationError("Error: Technical Advisor Must Be Recruited")
		elif self.is_ta_workplan_approved is False:
			raise ValidationError("Error: Technical Advisor Workplan Must Be Approved")
		elif self.is_microgrant_amount_approved is False:
			raise ValidationError("Error: Microgrant Must Be Approved By Regional Team")
		elif self.is_bank_detail_added is False:
			raise ValidationError("Error: Bank Details Must Be Added to Community Profile")
		elif self.is_measuring_success_approved is False:
			raise ValidationError("Error: Measuring Success Must Be Approved by Program Manager")

	def action_operational_action_plan(self):
		if self.is_implementation_action_plan_approved is True:
			self.state = 'operational_action_plan'
		elif self.is_implementation_action_plan_approved is False:
			raise ValidationError("Error: PM Must Approve Implementation Action Plan")

	def action_operational_budget(self):
		if self.is_implementation_budget_approved is True:
			self.state = 'operational_budget'
		elif self.is_implementation_budget_approved is False:
			raise ValidationError("Error: PM Must Approve Implementation Budget")

	def action_sustainability_plan(self):
		if self.is_operational_action_plan_approved is True:
			self.state = 'sustainability_plan'
		elif self.is_operational_action_plan_approved is False:
			raise ValidationError("Error: PM Must Approve Operational Action Plan")

	def action_transition_strategy(self):
		if self.is_operational_budget_approved is True:
			self.state = 'transition_strategy'
		elif self.is_operational_budget_approved is False:
			raise ValidationError("Error: PM Must Approve Operational Budget")

	def action_proposal_review(self):
		if (self.are_bylaws_acknowledged is True
			and self.is_sustainability_plan_approved is True):
			self.state = 'proposal_review'
			self.phase = 'planning'
		elif self.are_bylaws_acknowledged is False:
			raise ValidationError("Error: Community Must Acknowledge Bylaws")
		elif self.is_sustainability_plan_approved is False:
			raise ValidationError("Error: PM Must Approve Sustainability Plan")

	def action_grant_agreement(self):
		if (self.is_bank_account_open is True and
			self.is_proposal_approved_by_ta is True and
			self.is_proposal_approved_by_team is True and
			self.is_oca3_completed is True):
			self.state = 'grant_agreement'
			self.phase = 'implementation'
		elif self.is_proposal_approved_by_team is False:
			raise ValidationError("Error: Proposal Must Be Approved By Team/PM")
		elif self.is_proposal_approved_by_ta is False:
			raise ValidationError("Error: Proposal Must Be Approved By Technical Advisor")
		elif self.is_bank_account_open is False:
			raise ValidationError("Error: Community Bank Account Must Be Open")
		elif self.is_oca3_completed is False:
			raise ValidationError("Error: OCA3 Must Be Completed")


	def action_first_disbursement(self):
		if (self.is_receipt_book_received is True and
			self.is_disbursement_book_received is True and
			self.is_grant_agreement_translated is True and
			self.pg_signed_agreement is True):
			self.state = 'first_disbursement'
		elif self.is_grant_agreement_translated is False:
			raise ValidationError("Error: Grant Agreement Must Be Translated")
		elif self.pg_signed_agreement is False:
			raise ValidationError("Error: Planning Group Must Have Signed Grant Agreement")
		elif self.is_receipt_book_received is False:
			raise ValidationError("Error: Community Must Have Received Receipt Book")
		elif self.is_disbursement_book_received is False:
			raise ValidationError("Error: Community Must Have Received Disbursement Record Book")

	def action_project_management(self):
		if (self.is_microgrant_disbursed is True and
			self.is_microgrant_confirmed is True):
			self.state = 'project_management'
		elif self.is_microgrant_disbursed is False:
			raise ValidationError("Error: First Disbursement Must Be Disbursed")
		elif self.is_microgrant_confirmed is False:
			raise ValidationError("Error: Community Must Confirm MicroGrant Receipt")

	def action_leadership(self):
		self.state = 'leadership'

	def action_imp_transition_strategy(self):
		self.state = 'imp_transition_strategy'
		self.phase = 'implementation'

	def action_post_implementation(self):
		if (self.is_launch_approved_ta is True and
			self.is_capacity_verified is True and
			self.is_imp_action_plan_completed is True and
			self.is_ta_visits_verified is True and
			self.is_transition_strategy_completed is True):
			self.state = 'post_implementation'
			self.phase = 'post_implementation'
		elif self.is_launch_approved_ta is False:
			raise ValidationError("Error: Technical Advisor Must Approve Project Launch")
		elif self.is_capacity_verified is False:
			raise ValidationError("Error: PM must visit to verify community capacity in reocrd keeping and banking")
		elif self.is_imp_action_plan_completed is False:
			raise ValidationError("Error: Completion of Implementation Action Plan Activities Must Be Verified By TA")
		elif self.is_ta_visits_verified is False:
			raise ValidationError("Error: PM Must Verify Scheduled TA Visits Have Occurred")
		elif self.is_transition_strategy_completed is False:
			raise ValidationError("Error: Transition Strategy Must Be Complete")

	def action_graduation(self):
		if (self.is_all_mg_disbursed is True and
			self.are_all_receipts_collected is True and
			self.all_ta_trainings_occurred is True and
			self.all_pillar_trainings_occured is True and
			self.did_community_meet_pillars is True and
			self.is_exit_agreement_signed is True and
			self.did_community_report_progress is True and
			self.are_next_steps_established is True and
			self.are_transition_strategy_activities_completed is True):
			self.state = 'graduated'
			self.phase = 'graduated'
		elif self.is_all_mg_disbursed is False:
			raise ValidationError("Error: All Remaining MicroGrant Balance Must Be Disbursed")
		elif self.are_all_receipts_collected is False:
			raise ValidationError("Error: All Receipts Must Be Collected")
		elif self.all_ta_trainings_occurred is False:
			raise ValidationError("Error: All TA Trainings Must Have Occurred")
		elif self.all_pillar_trainings_occured is False:
			raise ValidationError("Error: All Pillar Trainings Must Have Occurred")
		elif self.is_exit_agreement_signed is False:
			raise ValidationError("Error: Exit Agreement Must Be Signed")
		elif self.did_community_report_progress is False:
			raise ValidationError("Error: Community Must Report On Progress Towards Communal Goal")
		elif self.are_next_steps_established is False:
			raise ValidationError("Error: Community Must Establish Next Steps Towards Their Goal")
		elif self.are_transition_strategy_activities_completed is False:
			raise ValidationError("Error: All Transition Strategy Activities Must Have Been Completed")
		elif self.did_community_meet_pillars is False:
			raise ValidationError("Error: Community Must Meet Minimum Pillar Thresholds")

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
	#      FCAP   Workflow Parameters Class           |
	#---------------------------------------------------
class CommunityWorkflowParameters(models.Model):
	_name = 'sparkit.communityworkflowparameters'

	name = fields.Char(string="Name")
	# Partnership -> Community Building
	#This variable defines the 'breakpoint' for % of community that signed the partnership agreement,
	# for example, a breakpoint of 100 households:
	# < 100 households = _% of community must have signed
	# > 100 households = _% of community must have signed
	partnership_hh_breakpoint = fields.Integer(string="Households Breakpoint",
		help="""This variable defines the 'breakpoint' for percentage of community that signed the partnership agreement, for example, a breakpoint of 100 households:
		< 100 households = __ percent of community must have signed
		=> 100 households = ___ of community must have signed""")
	# These variables define the percentage of households after the breakpoint
	partnership_hh_upper = fields.Float(string="Percent of HH Above Breakpoint that Must Sign Partnership Agreement")
	partnership_hh_lower = fields.Float(string="Percent of HH Below Breakpoint that Must Sign Partnership Agreement")

	# Community Building -> Goal Setting
	communitybldg_min_elected_leaders = fields.Integer(string="Minimum Number of Elected Leaders")
	communitybldg_max_elected_leaders = fields.Integer(string="Maximum Number of Elected Leaders")

	# Goals -> Objectives
	min_goals_brainstormed = fields.Integer(string="Minimum Number of Goals Brainstormed")
	min_pathways_brainstormed = fields.Integer(string="Minimum Number of Pathways Brainstormed")

	#------------------------------
	#  Validation and Constraints
	#------------------------------
	@api.constrains('partnership_hh_upper')
	def _check_partnership_hh_upper(self):
		for r in self:
			if r.parntership_hh_upper > 1:
				raise ValidationError("Error: Must be less than 1")

	@api.constrains('partnership_hh_lower')
	def _check_partnership_hh_upper(self):
		for r in self:
			if r.partnership_hh_lower > 1:
				raise ValidationError("Error: Must be less than 1")

	_sql_constraints = [
		#Unique Workfow
		('name_unique',
    	'UNIQUE(name)',
    	"The community name must be unique"),
    ]
