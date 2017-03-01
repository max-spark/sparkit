# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime

#Independent Projects

class OngoingCommunityAssessment(models.Model):
	_name = 'sparkit.oca'

	name = fields.Char(compute='_get_name', string="Form ID")
	country_id = fields.Many2one(related='community_id.country_id', string="1. Country", readonly=True)
	community_id = fields.Many2one('sparkit.community', string="2. Community")
	project_category_id = fields.Many2one(related='community_id.project_category_id',
		string="Project Category")
	project_subcategory_id = fields.Many2one(related='community_id.project_subcategory_id',
		string="Project SubCategory")
	project_category_name = fields.Char(related='project_category_id.name')
	project_subcategory_name = fields.Char(related='project_subcategory_id.name')
	date = fields.Date(string="3. Date of Assessment")
	collected_by = fields.Many2one('res.users', string="4. Collected By",
		default=lambda self: self.env.user)
	gps_coordinates_longitude = fields.Char(string="Longitude of OCA")
	gps_coordinates_latitude = fields.Char(string="Latitude of OCA")
	oca_number = fields.Selection(
		[('1', '1 - Community Identification: Basline/Scouting'),
		('2', '2 - Planning: Pathway Selection'),
		('3', '3 - Planning: Proposal Finalization'),
		('4', '4 - Post Implementation: Month 1'),
		('5', '5 - Post Implementation: Month 6'),
		('6', '6 - Post Implementation: Month 12'),
		('7', '7 - Post Implementation: Month 18'),
		('8', '8 - Post Implementation: Month 24')],
		select=True, string="5. Community Assessment Number",
		help="""Please select the Community Assessment number corresponding to the community's step:
		1. Scouting/Baseline
		2. After Pathway Selection
		3. After Proposal Finalization
		4. 1 Month Post Implementation
		5. 6 Months Post Implementation
		6. 12 Months Post Implementation
		7. 18 Months Post Implementation
		8. 24 Months Post Implementation """, required=True)
	start_time = fields.Float(string="Start Time")
	end_time = fields.Float(string="End Time")


	#Section One: Background
	#Todo: Add domain only allowing community members from the community
	community_member = fields.Char(string="6. Community Member", required=True)
	age = fields.Integer(string="7. Age")
	sex = fields.Selection([(0, 'Male'), (1, 'Female')], select=True,
		string="8. Sex")
	household_size = fields.Integer(string="9. Household Size")
	marital_status = fields.Selection([(1, 'Single'), (2, 'Married'), (3, 'Divorced'),
		(4, 'Widowed'), (5, 'Other')], string = "10. Marital Status")
	#TODO: Think About Better Way to Code this
	group_memberships = fields.Char(string="11. Group Memberships")

	#Biggest Concern
	biggestconcern_family = fields.Text(string="12. What is the biggest concern/most pressing need in your family?")
	biggestconcern_family_category_id = fields.Many2one('sparkit.biggestconcerncategory',
		string="12. Family's biggest concern/most pressing need - category")
	biggestconcern_family_subcategory_id = fields.Many2one('sparkit.biggestconcernsubcategory',
		string="12. Family's biggest concern/most pressing need - subcategory")
	biggestconcern_cmty= fields.Text(string="13. What is the biggest concern/most pressing need in your community?")
	biggestconcern_cmty_category_id = fields.Many2one('sparkit.biggestconcerncategory',
		string="13. Community's biggest concern/most pressing need - category")
	biggestconcern_cmty_subcategory_id = fields.Many2one('sparkit.biggestconcernsubcategory',
		string="13. Community's biggest concern/most pressing need - subcategory")

	#Section Two: Capacity
	capacity14 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "14. Are you comfortable being involved in making important decisions in your community?")
	capacity15 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "15. Do you have the skills needed to be involved in making decisions about important issues in your community?")
	capacity16 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "16. Together, does your community have the skills needed to make decisions about important issues that affect community?")
	capacity17 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "17. Do you believe your community can work together to successfully implement a project together?")
	capacity18 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "18. Do you have control over important decisions in your life?")


	#Section Three; Cohesion
	cohesion19 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "19. Do you feel comfortable joining any group/committee in your community?")
	cohesion20 = fields.Selection([(0,'No'), (1, 'Yes')], select=True,
		string= "20. Are there people in this community who do not feel comfortable joining groups/committees?")
	cohesion20_1 = fields.Char(string="20.1 - If yes, who?")
	cohesion21 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "21. Can your community resolve conflicts together?")
	cohesion22 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "22. Can your community work together to improve the community, even when you face challenges/difficulties/barriers?")
	cohesion23 = fields.Selection([(1,'None'), (2,'Low'), (3,'Moderate'), (4,'High'), (5,'Very High')], select=True,
		string = "23. In the last month, what has been the level of conflict in your community?")
	cohesion24 = fields.Selection([(1,'None'), (2,'Low'), (3,'Moderate'), (4,'High'), (5,'Very High')], select=True,
		string = "24. How important is it that your community work together to improve the community?")
	cohesion25 = fields.Selection([(1,'None'), (2,'Low'), (3,'Moderate'), (4,'High'), (5,'Very High')], select=True,
		string = "25. Do you believe there are benefits to working together as a community? What is an example?")
	cohesion26 = fields.Selection([(1,'None'), (2,'Low'), (3,'Moderate'), (4,'High'), (5,'Very High')], select=True,
		string = "26. Are your ideas and opinions taken into consideration in meetings?")
	cohesion27 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string = "27. Family?")
	cohesion28 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string = "28. Community Members?")
	cohesion29 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string = "29. Neighboring Community?")
	cohesion30 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string = "30. Group Members?")
	cohesion31 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string = "31. Community Leaders?")
	cohesion32 = fields.Integer(string="32. How many new people have you met since working with Spark?")

	#Section Four: Leadership
	leadership33 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "33. Do your leaders involve the community in making important decisions?")
	leadership34 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "34. Does your community tells your leaders when they feel they have made a mistake or done something wrong?")
	leadership35 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "35. Do you trust the leaders in your community?")
	leadership36 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "36. Do you have opportunities to be a leader in your community?")
	leadership37 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "37. Do you feel comfortable being a leader in your community?")

	#Section Five: Civic Engagement
	civic_engagement38 = fields.Selection([(0, 'No'), (1, 'Once'), (2, 'More Than Once')], select=True,
		string = "38. In the past one month, has your community worked together to solve a problem or reach a goal?")
	civic_engagement39 = fields.Selection([(0, 'Spark'), (1, 'Elected Leaders'), (2, 'Community/Planning Group'), (3, 'Other')],
		string = "39. Who is responsible for the success of your community’s work together?")
	civic_engagement40 = fields.Selection([(0, 'No'), (1, 'One'), (2, 'More Than One')], select=True,
		string = "40. Are you involved in groups/committees in your community?")
	civic_engagement41 = fields.Selection([(1,'Strongly Disagree'), (2,'Disagree'), (3,'Neutral/Unsure'), (4,'Agree'), (5,'Strongly Agree')], select=True,
		string = "41. Is it important for you to be involved in making important decisions in your community?")
	civic_engagement42 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string = "42. Have you contributed to implementation of the project? If so, how?")
	civic_engagement_42_1 = fields.Text(string="42.1 How have you contributed to implementation?")

	# Cross Sector
	baseline_owns_land = fields.Boolean(string="Land?")
	baseline_owns_soap = fields.Boolean(string="Soap?")
	baseline_owns_mattress = fields.Boolean(string="Bed/Mattress?")
	baseline_owns_radio = fields.Boolean(string="Radio?")
	baseline_owns_bike = fields.Boolean(string="Bicycle?")
	baseline_owns_phone = fields.Boolean(string="Cell Phone or Telephone?")
	baseline_owns_lights = fields.Boolean(string="Electric Lights")
	# can we add this
	baseline_owns_solar = fields.Boolean(string="Solar Power? (panels)")
	baseline_owns_television = fields.Boolean(string="Television?")
	baseline_owns_motorcycle = fields.Boolean(string="Motorcycle?")
	baseline_owns_nothing = fields.Boolean(string="Does Not Own Any Items")
	total_baseline_items = fields.Integer(string="1b. If you do own any of these items, how many of these items IN TOTAL do you own?")

	owns_land = fields.Boolean(string="Land?")
	owns_soap = fields.Boolean(string="Soap?")
	owns_mattress = fields.Boolean(string="Bed/Mattress?")
	owns_radio = fields.Boolean(string="Radio?")
	owns_bike = fields.Boolean(string="Bicycle?")
	owns_phone = fields.Boolean(string="Cell Phone or Telephone?")
	owns_lights = fields.Boolean(string="Electric Lights")
	# can we add this
	owns_solar = fields.Boolean(string="Solar Power? (panels)")
	owns_television = fields.Boolean(string="Television?")
	owns_motorcycle = fields.Boolean(string="Motorcycle?")
	owns_nothing = fields.Boolean(string="Does Not Own Any Items / Unable to purchase as a result of the FCAP")
	total_items_purchased = fields.Integer(string="2b. If you were able to purchase items, how many of these items IN TOTAL were you able to purchase as a result of working with Spark?")

	baseline_owns_goat = fields.Boolean(string="Goat?")
	baseline_owns_sheep = fields.Boolean(string="Sheep?")
	baseline_owns_cow = fields.Boolean(string="Cow?")
	baseline_owns_pig = fields.Boolean(string="Pig?")
	baseline_owns_chicken = fields.Boolean(string="Chicken?")
	baseline_owns_other = fields.Boolean(string="Other Animal?")
	total_baseline_animals = fields.Integer(string="3b. If you do own animals, how many animals do you own?")

	animals_purchased_ids = fields.Many2many('sparkit.crosssectoranimal',
		string="3c. If you were able to purchase animals as a result of working with Spark, what animals were they?")

	purchased_goat = fields.Boolean(string="Goat?")
	purchased_sheep = fields.Boolean(string="Sheep?")
	purchased_cow = fields.Boolean(string="Cow?")
	purchased_pig = fields.Boolean(string="Pig?")
	purchased_chicken = fields.Boolean(string="Chicken?")
	purchased_other = fields.Boolean(string="Other Animal?")
	total_purchased_animals = fields.Integer(string="3d. If you were able to purchase additional animals as a result of working with Spark, how many?")

	education_access = fields.Selection([(0, 'Not Able to Cover Any Cost'), (1, 'Able to Cover Some Cost'), (2, 'Able to Cover All Cost'), (99, 'Does Not Have Children')],
		select=True, string="4. This past school term, what was your ability to pay the costs associated with your children’s education?")

	illnesses_last_month_ids = fields.Many2many('sparkit.crosssectorillness',
		string="5. In the past month, have any household members suffered from any of the following illnesses? Please choose all that apply.")

	health_access = fields.Selection([(1, 'Always'), (2, 'Sometimes'), (3, 'Rarely'), (4, 'Never')], select=True,
		string="6. When someone in your household is sick, is your household able to pay for treatment without help?")


	# Project Specific Questions - hidden depending on community's project category

	#Agriculture
	agriculture_individual_benefit = fields.Selection([(0, 'no'),
		(1, 'a little'), (2, 'a lot')], select=True,
		string="60. Have you benefited from the community’s agriculture project?")
	agriculture_individual_benefits_examples = fields.Text(
		string="60a. Please list examples of individual benefits.")
	agriculture_community_benefit = fields.Selection([(0, 'no'),
		(1, 'a little'), (2, 'a lot')], select=True,
		string="61. Has the community benefited from the community’s agriculture project?")
	agriculture_community_benefits_examples = fields.Text(
		string="61a. Please list examples of community benefits.")


	#Animal Rearing
	animalrearing_individual_benefit = fields.Selection([(0, 'no'),
		(1, 'a little'), (2, 'a lot')], select=True,
		string="50. Have you benefited from the community’s animal rearing project?")
	animalrearing_individual_benefits_examples = fields.Text(
		string="50a. Please list examples of individual benefits.")
	animalrearing_community_benefit = fields.Selection([(0, 'no'),
		(1, 'a little'), (2, 'a lot')], select=True,
		string="51. Has the community benefited from the community’s animal rearing project?")
	animalrearing_community_benefits_examples = fields.Text(
		string="51a. Please list examples of community benefits.")


	#Vocational
	vocational_individual_benefit = fields.Selection([(0, 'no'),
		(1, 'a little'), (2, 'a lot')], select=True,
		string="30. Have you benefited from the community’s vocational school project?")
	vocational_individual_benefits_examples = fields.Text(
		string="30a. Please list examples of individual benefits.")
	vocational_community_benefit = fields.Selection([(0, 'no'),
		(1, 'a little'), (2, 'a lot')], select=True,
		string="31. Has the community benefited from the community’s vocational school project?")
	vocational_community_benefits_examples = fields.Text(
		string="31a. Please list examples of community benefits.")


	#Infrastructure
	infrastructure_primary_energy_source = fields.Selection([(1, 'Solid Fuel'),
		(2, 'Electricity'), (3, 'Gas Tank'), (4, 'Petrol'), (5, 'Solar Power'),
		(6,'Other'), (99, 'No Access')], select=True,
		string="70. What is your primary source of energy/power?")

	infrastructure_other_sources = fields.Text(
		string="71. If you use other energy/power sources, which one(s)?")

	infrastructure_spark = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string="72. Have your energy sources changed as a result of the project with Spark?")

	water_primary_source = fields.Selection([(1, 'Protected Tap'),
		(2, 'Bore Hole'), (3, 'Protected Well'), (4, 'Unprotected Well'),
		(5, 'Lake Water'), (6, 'Rain Water'), (7, 'Other')], select=True,
		string="73. What is your primary source of water?")

	clean_water_access_home = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string="74. Do you have access to clean water in your home?")

	clean_water_access_community = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string="75. Do you have access to clean water in your community?")

	clean_water_spark = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string="76. Has your access to clean water at home or in the community changed as a result of the project with Spark?")

	#Nursery
	nursery40 = fields.Selection([(99, '0'),
		(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
		(8, '8'), (9, '9'), (10, '10'), ('over10', 'Over 10')], select=True,
		string="40. How many nursery age children live in your household?")

	nursery41 = fields.Selection([(99, '0'), (999, 'All'),
		(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
		(8, '8'), (9, '9'), (10, '10'), ('over10', 'Over 10')], select=True,
		string="41. Of these children, how many are enrolled in the nursery school?")

	nursery42 = fields.Selection([(1, 'Cannot Pay School Fees'),
		(2, 'Cannot Pay Other Expenses (uniforms, materials, transportation, other school related expenses)'),
		(3, 'Child Needed at Home'), (4, 'Illness'), (5, 'Other Reason'),
		(99, 'No Nursery Aged Children'), (999, 'All Nursery Aged Children Enrolled')],
		select=True,
		string="42. If there are some nursery aged children in the household that are not enrolled, what is the reason?")

	#Health
	health20 = fields.Selection([(1, 'Less than Three Months Ago'),
		(2, 'Between 3 and 6 Months'), (3, 'Between 6 months and 1 year'),
		(4, 'Between 1 year and 2 years'), (5, 'More than 2 years ago'),
		(6, 'Never Needed')], select=True,
		string="20. When was the last time someone in your household needed health care?")

	health21 = fields.Selection([(1, 'Hospital'), (2, 'Outpatient Facility (health clinic, health center, health post)'),
		(3, 'Pharmacy'), (4, 'Private Physician'), (5, 'Traditional Healer'),
		(6, 'Other')], select=True,
		string = "21. If they received health care, where did they receive care?")

	health22 = fields.Selection([(1, 'Cost'), (2, 'Transport'), (3, 'Inadequate Staff'),
		(4, 'Inadequate Facility or Medication'), (5, 'Did not seek health care'),
		(6, 'Did not think they were sick'), (7, 'Denied Healthcare'),
		(8, 'Did not know where to go'), (9, 'Other')], select=True,
		string = "22. If they did not receive health care, what was the primary reason?")

	#Sanitation
	sanitation10 = fields.Selection([(1, 'In My Community'), (2, 'Shared with One or More Households'),
		(3, 'Shared with Only Those in My Household'), (4, 'Other'), (99, 'No Access')], select=True,
		string="10. What is your current access to sanitation – pit latrines?")

	sanitation11 = fields.Selection([(1, 'In My Community'), (2, 'Shared with One or More Households'),
		(3, 'Shared with Only Those in My Household'), (4, 'Other'), (99, 'No Access')], select=True,
		string="11. What is your current access to sanitation – handwasing?")

	sanitation12 = fields.Selection([(1, 'In My Community'), (2, 'Shared with One or More Households'),
		(3, 'Shared with Only Those in My Household'), (4, 'Other'), (99, 'No Access')], select=True,
		string="12. What is your current access to sanitation – bathing houses?")

	sanitation13 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string="13. Do you have access to plate stands?")

	sanitation14 = fields.Selection([(0, 'No'), (1, 'Yes')], select=True,
		string="14. Do you have access to sanitation/health training?")

	sanitation15 = fields.Text(string="What other sanitation resources do you have access to?")


	@api.multi
	@api.depends('community_id', 'oca_number', 'community_member')
	def _get_name(self):
		for r in self:
			r.name = r.community_id.name + ' - ' + r.community_member + ': OCA ' + str(r.oca_number)


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


	#---------------------------------------------
	#
	#   Cross sector categories
	#
	#
	#---------------------------------------------

class CrossSectorItem(models.Model):
	_name = 'sparkit.crosssectoritem'

	name = fields.Char(string="Name")
	code = fields.Integer(string="Code")
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
