# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime

class OngoingCommunityAssessment(models.Model):
	_name = 'sparkit.oca'

	name = fields.Char(compute='_get_name', string="Form ID")
	country_id = fields.Many2one(related='community_id.country_id', string="Country", readonly=True)
	country_name = fields.Char(compute='_get_country_name', string="Country Name", store=True)
	community_id = fields.Many2one('sparkit.community', string="Community",
		ondelete='cascade')
	date = fields.Date(string="Date of Assessment")
	collected_by_new = fields.Char(string="Collected By")
	oca_number = fields.Selection(
		[('0', 'Baseline'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('graduated', 'Follow-up with Graduated Community')],
		select=True, string="OCA Number")
	oca_type = fields.Selection([('long', 'Long'), ('monitoring', 'Monitoring')], select=True, string="OCA Type")
	district = fields.Char(string="District")
	start_time = fields.Float(string="Start Time")
	end_time = fields.Float(string="End Time")
	odk_id = fields.Char(string="ODK ID")

	#Background
	community_member = fields.Char(string="Community Member")
	age = fields.Integer(string="Age")
	sex = fields.Selection([(0, 'Male'), (1, 'Female')], select=True,
		string="Sex")
	household_size = fields.Integer(string="Household Size")
	marital_status = fields.Selection([(1, 'Single'), (2, 'Married'), (3, 'Divorced'), (4, 'Widowed'), (5, 'Other')], string = "Marital Status")
	household_head = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Are you the head of your household?")
	family_head = fields.Selection([(1, 'Man'), (2, 'Woman'), (3, 'Orphan')], string = "If no, who is the head of your household?")
	leadershipstatus = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Are you part of your community's leadership?")

	#Biggest Concern
	biggestconcern_family = fields.Text(string="What is the biggest concern/most pressing need in your family?")
	biggestconcern_family_category_id = fields.Many2one('sparkit.biggestconcerncategory', string="What is the biggest concern/most pressing need in your family? -category")
	biggestconcern_family_subcategory_id = fields.Many2one('sparkit.biggestconcernsubcategory', string="What is the biggest concern/most pressing need in your family? -specific")
	biggestconcern_cmty= fields.Text(string="What is the biggest concern/most pressing need in your community?")
	biggestconcern_cmty_category_id = fields.Many2one('sparkit.biggestconcerncategory',	string="What is the biggest concern/most pressing need in your community? - category")
	biggestconcern_cmty_subcategory_id = fields.Many2one('sparkit.biggestconcernsubcategory', string="What is the biggest concern/most pressing need in your community? - specific")

	#Capacity
	capacity3_communalgoals = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Does your community have a formal long-term goal that was decided on collectively?")
	capacity_goaldescribe = fields.Text(string="If yes, what is this vision or goal?")
	capacity_goalvillageplanning = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "If yes, is this goal part of the village planning process?")
	capacity_goalinvolvement = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "If yes, was your household involved in the decision of selecting this vision or goal?")
	capacity3_1 = fields.Text(string="Please describe the goal(s) that your community has.")
	capacity4_goalinvolvement = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "If yes, was your household involved in the decision of selecting this goal?")
	capacity18_communalprojectsubedehe = fields.Integer(string="In the past year, has your community had any community projects that were supported by Ubedehe funds?")
	capacity18_ubedeheprojects = fields.Many2many('sparkit.communalprojects', string="If yes, what type(s) of project(s)?")
	capacity18_ubedeheother = fields.Char(string="If other, please specify.")
	capacity18_communalprojects = fields.Integer(string="Does your community have any other independent communal projects that are currently operational?")
	capacity1_communalprojects = fields.Integer(string="Does your community have any communal projects that are currently operational?")
	capacity1_1 = fields.Many2many('sparkit.communalprojects', string="If yes, what type(s) of project(s)?")
	capacity1_1_other = fields.Char(string="If other, please specify.")
	capacity2_contribute = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Has your household contributed to the implementation of any communal project(s)?")
	capacity2_1 = fields.Many2many('sparkit.householdcontribution', string="Please describe how your household has contributed.")
	capacity2_1_other = fields.Char(string="If other, please specify.")

	#Cohesion
	cohesion5_conflictlevel = fields.Integer(string="In the past 6 months, how many community-wide conflicts have there been?")
	cohesion5_1conflictresolved = fields.Integer(string="How many of these conflicts have been resolved?")
	leadership6_opportunities = fields.Selection(
		[('1', 'Strongly disagree'),
		('2', 'Disagree'),
		('3', "I don't know"),
		('4', 'Agree'),
		('5', 'Strongly agree')],
		select=True, string="In the past 6 months, have you had opportunities to be a leader in your community?")
	leadership7_responsibilities = fields.Many2many('sparkit.leadershipresponsibilities', string="In the past 6 months, have you volunteered to take on any responsibilities in your community?")
	leadership7_1 = fields.Text(string="If other, please describe.")

	#Civic Engagement - Independent Meetings
	ce8_indmeetings = fields.Selection(
		[('99', "I don't know"),
		('1', 'Never'),
		('2', 'Meets infrequently'),
		('3', 'Once a month'),
		('4', 'Twice a month'),
		('5', 'Weekly')],
		select=True, string="In the past 6 months, how often has your community met? (independently of Spark)")	
	ce8_1 = fields.Text(string="Please describe what type of meetings these are.")
	ce9_indmeetingsattend = fields.Selection(
		[('999', "Commmunity does not meet"),
		('1', 'Never'),
		('2', 'Rarely'),
		('3', 'Sometimes'),
		('4', 'Often'),
		('5', 'Always'),
		('99', "I don't know")],
		select=True, string="In the past 6 months, how often have you or someone from your household attended (non-Spark) community meetings?")	
	ce9_1 = fields.Selection(
		[('0', "No one (Household does not attend community meetings/Community does not meet)"),
		('1', 'Me (respondent)'),
		('2', 'Spouse'),
		('3', 'Child'),
		('4', 'Household head (if respondent is not the household head)'),
		('5', 'Other')],
		select=True, string="From your household, who normally attends these meetings?")	
	ce9_2_other = fields.Char(string="If other, please specify.")
	ce10_indparticipation = fields.Selection(
		[('999', "Does not attend meetings/community doesn't meet"),
		('1', 'Never (attends but does not participate)'),
		('2', 'Rarely'),
		('3', 'Sometimes'),
		('4', 'Often'),
		('5', 'Always'),
		('99', "I don't know")],
		select=True, string="In the past 6 months, how often have you spoken in (non-Spark) community meetings?")	

	#Civic Engagement - Spark-led Meetings
	ce11_Sparkattend = fields.Selection(
		[('999', "Commmunity does not meet"),
		('1', 'Never'),
		('2', 'Rarely'),
		('3', 'Sometimes'),
		('4', 'Often'),
		('5', 'Always'),
		('99', "I don't know")],
		select=True, string="In the past 6 months, how often have you or someone from your household attended Spark-led community meetings?")	
	ce11_1 = fields.Selection(
		[('0', "No one (Household does not attend community meetings/Community does not meet)"),
		('1', 'Me (respondent)'),
		('2', 'Spouse'),
		('3', 'Child'),
		('4', 'Household head (if respondent is not the household head)'),
		('5', 'Other')],
		select=True, string="From your household, who normally attends these Spark-led meetings?")	
	ce11_1_other = fields.Char(string="If other, please specify.")
	ce12_Sparkparticipation = fields.Selection(
		[('999', "Does not attend meetings/community doesn't meet"),
		('1', 'Never (attends but does not participate)'),
		('2', 'Rarely'),
		('3', 'Sometimes'),
		('4', 'Often'),
		('5', 'Always'),
		('99', "I don't know")],
		select=True, string="In the past 6 months, how often have you spoken in Spark-led community meetings?")	
	cohesion13_ideasopinions = fields.Selection(
		[('1', 'Never'),
		('2', 'Rarely'),
		('3', 'Sometimes'),
		('4', 'Often'),
		('5', 'Always')],
		select=True, string="Have your ideas been taken into consideration by your community leaders during meetings?")	
	ce14_decisioninvolvement = fields.Selection(
		[('1', 'No'),
		('3', 'Once'),
		('5', 'More than once')],
		select=True, string="In the past 6 months, have you helped make a decision in your community?")
	ce14_1 = fields.Text(string="Please describe.")
	ce15_workingtogethergoal = fields.Selection(
		[('1', 'No'),
		('3', 'Once'),
		('5', 'More than once')],
		select=True, string="In the past 6 months, has your community worked together to reach a (common) goal?")
	ce15_1 = fields.Text(string="If yes, please describe.")
	ce17_responsibles = fields.Selection(
		[('1', 'NGOs like (Spark/ACA)'),
		('2', 'Elected leaders'),
		('3', 'Community'),
		('4', 'Other')],
		select=True, string="Who is responsible for the success of your community working together?")
	ce17_1 = fields.Text(string="If other, please specify.")
	ce18_groups = fields.Selection(
		[('1', 'No'),
		('3', 'Once'),
		('5', 'More than once')],
		select=True, string="Are you involved in groups/committees in your community?")
	ce18_1 = fields.Text(string="If yes, please describe.")	

	#Advocacy
	advocacy19 = fields.Integer(string="In the past 6 months, how many times have you or someone in your community approached an outside organization for support?")
	advocacy19_1success = fields.Integer(string="How many of these have been successful?")
	advocacy20_what = fields.Text(string="What did you reach out for?")
	advocacy21_who = fields.Char(string="Who did you approach?")

	#Finances
	savings_methods = fields.Many2many('sparkit.savingsmethods', string="Which of the following methods is your household using to save?")	
	savings_other = fields.Text(string="If other, please specify.")
	money_in_account = fields.Integer(string="Approximately how much are you saving each month?")
	finance20_cmtybankaccount = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Does your community have a village bank account?")
	finance_accountuse = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Has the bank account been used in the past year?")
	finance_fundspurpose = fields.Text(string="What were the funds used for?")
	finance20_cmtybankaccount = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Does your community have a bank account?")
	finance21_cmtyupdates = fields.Selection(
		[('999', "No bank account exists"),
		('99', "I don't know"),
		('1', 'Never'),
		('2', 'Once a year'),
		('3', 'Once a month'),
		('4', 'Twice a month'),
		('5', 'Weekly')],
		select=True, string="If yes, how often do your leaders update you on communal funds in the bank account?")
	finance22_cmtybalance = fields.Integer(string="If yes, what is the balance on your community's bank account?")
	finance23_cmtysavings = fields.Selection(
		[('99', "I don't know"),
		('0', 'No'),
		('1', 'Community savings group'),
		('2', "Women's savings group"),
		('3', 'Elderly savings group'),
		('4', 'Other')],
		select=True, string="Does your community have any savings groups?")
	finance23_1 = fields.Char(string="If other, please specify.")
	finance24_cmtysavingsmember = fields.Selection(
		[('99', "I don't know"),
		('0', 'No'),
		('1', 'Community savings group'),
		('2', "Women's savings group"),
		('3', 'Elderly savings group'),
		('4', 'Other')],
		select=True, string="If yes, are you a member of any of these savings groups in your community?")
	finance25_cmtysavingsmtgs = fields.Selection(
		[('99', "I don't know"),
		('1', 'Never'),
		('2', 'Meets infrequently'),
		('3', 'Once a month'),
		('4', 'Twice a month'),
		('5', 'Weekly')],
		select=True, string="If yes, how often does your savings group meet?")
	finance26_cmtysavingscontribute = fields.Integer(string="If yes, how much do you contribute each week?")

	#Financial Planning and Training
	finance27_budget = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Does your household currently create a monthly plan or budget?")
	finance28_discuss = fields.Selection(
		[('1', 'Never'),
		('2', 'Once a year'),
		('3', 'Monthly'),
		('4', 'Weekly'),
		('5', 'Daily')],
		select=True, string="In the past year, how often has your household discussed how to use its money?")
	finance29_decisions = fields.Selection(
		[('1', 'Only the household head'),
		('2', 'Household head and spouse'),
		('3', 'Multiple adult family members (more than the household head and spouse)'),
		('4', 'The entire household'),
		('99', 'Other')],
		select=True, string="In your household, who is involved in decisions on how to use your household's money?")
	finance29_1 = fields.Char(string="If other, please specify.")
	finance30_training = fields.Selection(
		[('1', 'No'),
		('3', 'One'),
		('5', 'More than one')],
		select=True, string="Have you or anyone in your household participated in trainings on finance skills in the past?")
	finance30_1 = fields.Selection(
		[('1', 'Over a year ago'),
		('2', 'Within the past year'),
		('3', 'Within the past 6 months'),
		('4', 'Within the past 3 months'),
		('5', 'Within the past month')],
		select=True, string="If yes, when?")
	finance30_2describe = fields.Text(string="If yes, please describe the training you received.")

	#Cross-sectoral - Items
	cs31_itemsowned = fields.Many2many('sparkit.crosssectoritem', string="How many of the following do you own?")		
	cs31_1_numitemsowned = fields.Integer(string="Total # of items community member owns")

	#Cross-sectoral - Animals
	pi_agproduce = fields.Selection(
		[('did_not_farm', 'No member farmed or raised animals'),
		('farmed_only', 'Farmed only (no poultry or cattle)'),
		('farmed_and_poultry', 'Farmed and raised poultry'),
		('farmed_and_cattle', 'Farmed and raised cattle'),
		('farmed_poultry_cattle', 'Farmed and raised poultry and cattle')],
		select=True, string="In the past 12 months, has any household member grown food or other agricultural produce to eat or sell or raised cattle or poultry?")
	livestock = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Do you own any livestock?")
	goat = fields.Integer(string="Goat")
	sheep = fields.Integer(string="Sheep")
	cow = fields.Integer(string="Cow")
	pig = fields.Integer(string="Pigs")
	chicken = fields.Integer(string="Chicken")
	rabbit = fields.Integer(string="Rabbit")
	other = fields.Integer(string="Other")

	#Cross-sectoral - Food Security
	cs34_foodsecurity = fields.Integer(string="How many meals do you eat per day?")
	cs35_income = fields.Selection(
		[('0', 'None (unemployed)'),
		('1', 'farming (for own household)'),
		('2', 'commercial farming (farming for others)'),
		('3', 'self-employed/personal business (non-farming)'),
		('4', 'formal employment'),
		('5', 'other')],
		select=True, string="What is your households primary source of income?")
	cs35_1 = fields.Char(string="If other, please specify.")

	#Poverty Index
	pi_youth = fields.Integer(string="How many household members are 18-years-old or less?")
	pi_agactivity = fields.Integer(string="In the last 12 months, how many household members carried out any agricultural activity (whether farming, livestock, fishing, or forestry) for salary, wages, or in-kind compensation?")
	pi_nonfarm = fields.Integer(string="In the last 12 months, how many household members ran or operated a non-farm business for cash or profit for themselves, such as a small shop or other income-generating activity?")
	pi36_school = fields.Integer(string="How many household members are 6-12 years old?")
	pi36_school_1 = fields.Integer(string="How many household members between 6-12 years old are in school?")
	pi_read = fields.Selection(
		[('no', 'No'),
		('no_female_head', 'No female head/spouse in the household'),
		('yes', 'Yes')],
		select=True, string="Can the (oldest) female head/spouse read a letter or a simple note (regardless of language), or has she completed at least Primary 1?")
	pi37_read = fields.Selection(
		[('no', 'No'),
		('no_female_head', 'No female head/spouse in the household'),
		('yes', 'Yes')],
		select=True, string="Can the (oldest) female head of household/spouse read and write with understanding in any language?")
	pi38_wall = fields.Selection(
		[('unburnt_bricks_wall', 'Unburnt bricks with mud'),
		('mud_poles_wall', 'Mud and Poles'),
		('other_wall', 'Other'),
		('unburnt_bricks_cement_wall', 'Unburnt bricks with cement'),
		('wood_wall', 'Wood'),
		('tin_wall', 'Tin/Iron Sheets'),
		('concrete_wall', 'Concrete/stones'),
		('burnt_bricks_wall', 'Burnt stabilized bricks'),
		('cement_blocks_wall', 'cement_blocks_wall')],
		select=True, string="What type of material is mainly used for the construction of the wall of the dwelling?")
	pi39_roof = fields.Selection(
		[('roof_thatch', 'Thatch'),
		('roof_tins', 'Tins'),
		('roof_iron_sheets', 'Iron Sheets'),
		('roof_concrete', 'Concrete'),
		('roof_tiles', 'Tiles'),
		('roof_asbestos', 'Asbestos'),
		('roof_other', 'Other')],
		select=True, string="What type of material is mainly used for the construction of the roof of the dwelling?")
	pi_lighting = fields.Selection(
		[('lighting_firewood', 'Firewood'),
		('lighting_batteries', 'Batteies and bulb'),
		('lighting_biogas', 'Biogas'),
		('lighting_lantern', 'Lantern (agatadowa)'),
		('lighting_candle', 'Candle'),
		('lighting_oil_lamp', 'Oil lamp'),
		('lighting_electricity', 'Electricity (from any source)'),
		('lighting_generator', 'Generator'),
		('lighting_solar', 'Solar Panel'),
		('lighting_other', 'Other')],
		select=True, string="What is the main source of lighting in the residence of the household?")
	pi_beds = fields.Integer(string="How many mattresses does your household own?")
	pi40_cooking = fields.Selection(
		[('firewood_cooking', 'Firewood'),
		('cow_dung_cooking', 'Cow dung'),
		('grass_cooking', 'Grass (reeds)'),
		('charcoal_cooking', 'Charcoal'),
		('paraffin_stove_cooking', 'Paraffin Stove'),
		('gas_cooking', 'Gas'),
		('electricity_cooking', 'Electricity (regardless of source)'),
		('biogas_cooking', 'Biogas'),
		('other_cooking', 'Other')],
		select=True, string="What is the main source of energy used for cooking?")
	pi41_toilet = fields.Selection(
		[('toilet_none', 'No facility/bush'),
		('toilet_polythene', 'Polythene bags'),
		('toilet_bucket', 'Bucket'),
		('toilet_uncovered', 'Uncovered pit latrine (with or without slab)'),
		('toilet_compost', 'Ecosan (compost toilet)'),
		('toilet_covered_witout_slab', 'Covered pit latrine without slab'),
		('toilet_covered_with_slab', 'Covered pit latrine with slab'),
		('toilet_flush', 'VIP latrine, ro flush toilet'),
		('toilet_other', 'Other')],
		select=True, string="What type of toilet facility does the household use?")
	pi42_phones = fields.Integer(string="How many mobile phones do members of your household own?")
	pi43_radio = fields.Integer(string="Does any member of your household own a radio?")
	pi44_shoes = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Does every member of the household have at least one pair of shoes?")

	#Rwanda Specific
	number_of_dependant = fields.Integer(string="How many dependants do you have?")
	school_children = fields.Integer(string="How many school-aged children are in your household?")
	school_dropouts = fields.Integer(string="Of the school-aged children in your household, how many are not currently enrolled school?")
	special_groups = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Is there anyone in the household who is disabled?")
	ubudehe_category = fields.Selection(
		[('1', 'First'),
		('2', 'Second'),
		('3', 'Third'),
		('4', 'Forth'),
		('99', "I don't know")],
		select=True, string="Which Ubudehe category does your household belong to?")
	direct_support = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Has your household ever received direct support from the government?")
	vup_payment = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Has your household ever received payment for VUP work?")
	ubudehe_fund = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Did your household receive Ubudehe funds/support this year?")
	girinka_recipient = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Is your household a Girinka recipient?")
	health_insurance = fields.Selection(
		[('0', 'Not at all'),
		('1', 'Yes, paid all by self-employed'),
		('2', 'Yes, through government subsidies'),
		('3', 'Yes, through village loan'),
		('4', 'Yes, through other (non-government) sponsors'),
		('99', "Other")],
		select=True, string="This year, were you able to afford paying health insurance for your family?")
	health_other = fields.Char(string="If other, please specify.")
	kitchen_garden = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Does your household have a kitchen garden?")
	latrines = fields.Selection(
		[('0', 'No access'),
		('1', 'Shares latrine with few others'),
		('2', 'Shares latrine with many others'),
		('3', 'Household has own latrine')],
		select=True, string="What is your household's access to a latrine?")

	#Verification Questions
	grant_check = fields.Char(string="What was your grant size? (for the Spark project)")
	disbursed_check = fields.Char(string="How much of your grant has been disbursed?")
	projecttype_check = fields.Char(string="What is your community's project?")
	ta_check = fields.Char(string="What is the name of your technical advisor?")
	use_contact_info = fields.Selection([(0, 'No'), (1, 'Yes'), (99, "I don't know")], string = "Should we need to contact you in the future, can we use your telephone contact?")
	interviewee_contact = fields.Char(string="Contact")



	@api.multi
	@api.depends('community_id', 'oca_number')
	def _get_name(self):
		for r in self:
			r.name = r.community_id.name + ' - OCA ' + str(r.oca_number)

	@api.depends('country_id')
	def _get_country_name(self):
		for r in self:
			if r.country_id:
				r.country_name = r.country_id.name

	#---------------------------------------------
	#
	#   Biggest Concern categories/subcategories
	#	for OCA questions 12/13
	#
	#---------------------------------------------


class BiggetConcernCategory(models.Model):
	_name = 'sparkit.biggestconcerncategory'

	name = fields.Char(string="Name")
	category_code = fields.Integer(string="Code")
	subcategory_ids = fields.One2many('sparkit.biggestconcernsubcategory', 'category_id',
		string="Sub-Categories")


	_sql_constraints = [
		#Unique Code
		('code_unique',
    	'UNIQUE(category_code)',
    	"The code must be unique"),
    ]


class BiggestConcernSubCategory(models.Model):
	_name = 'sparkit.biggestconcernsubcategory'

	name = fields.Char(string="Name")
	subcategory_code = fields.Integer(string="Code")
	category_id = fields.Many2one('sparkit.biggestconcerncategory',
		string="Biggest Concern Category")


	_sql_constraints = [
		#Unique Code
		('code_unique',
    	'UNIQUE(subcategory_code)',
    	"The code must be unique"),
    ]


class CrossSectorItem(models.Model):
	_name = 'sparkit.crosssectoritem'

	name = fields.Char(string="Name")
	code = fields.Char(string="Code")
	filter = fields.Integer(string="Filter: 1-Spark, 0-Baseline")


class CrossSectorAnimal(models.Model):
	_name = 'sparkit.crosssectoranimal'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")
	filter = fields.Integer(string="Filter: 1-Spark: 0-Baseline")


class CrossSectorIllness(models.Model):
	_name = 'sparkit.crosssectorillness'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")


class Communalprojects(models.Model):
	_name = 'sparkit.communalprojects'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")	


class Householdcontribution(models.Model):
	_name = 'sparkit.householdcontribution'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")


class Leadershipresponsibilities(models.Model):
	_name = 'sparkit.leadershipresponsibilities'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")


class Savingsmethods(models.Model):
	_name = 'sparkit.savingsmethods'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")
