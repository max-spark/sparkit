# -*- coding: utf-8 -*-

#TODO Automatically fill in final proposal using workflow?

from openerp import models, fields, api

class CommunityProposal(models.Model):
    _name = 'sparkit.communityproposal'

    name = fields.Char(compute='_get_name')
    community_id = fields.Many2one('sparkit.community', string="Community")
    facilitator_id = fields.Many2one('res.users', string="Facilitator")
    project_id = fields.Many2one('sparkit.sparkproject', string="Project")

    #----  Proposal  -------
    # Q1. Background
    community_background = fields.Text(string="1. Community Background")
    goals = fields.Text(string="1a. What are the priority goals the community has set, and why?")
    objectives_identified = fields.Text(string="1b. What are the objectives the community identified? What is their current progress?",
        help="""What are the different objectives that the community identified? What is the community’s current progress toward each objective?""")
    objectives_chosen = fields.Text(string="1c. What objective is the community focusing on, and how do they know if it will be most impactufl towards their goal?")

    # Q2. Pathways
    pathways_identified = fields.Text(string="2a. What are the different pathways identified?")
    pathways_chosen = fields.Text(string="2b. What is the one pathway chosen to be followed? ")
    pathway_desc = fields.Text(string="2c. How will that pathway help community to reach their goal?")

    # Q3. Participatory M&E
    pme_ids = fields.One2many('sparkit.proposalpme', 'proposal_id', limit=3, string="PM&E")

    # Q4. Implementation Action Plan
    implementation_activities_ids = fields.One2many('sparkit.proposalactivities', 'proposal_id', string="Proposal Activities")

    # Q5. Implementation Budget
    implementation_budget_ids = fields.One2many('sparkit.proposalbudget', 'proposal_id', string="Budget Items")

    # Q6. Operational Action Plan
    operational_activities_ids = fields.One2many('sparkit.operationalactivities', 'proposal_id', string="Operational Activities")

    # Q7. Operational Budget
    operational_budget_profits_ids = fields.One2many('sparkit.operationalprofit', 'proposal_id',
        string="Operational Budget - Profit")
    operational_budget_expenditure_ids = fields.One2many('sparkit.operationalexpenditure', 'proposal_id',
        string="Operational Budget - Expenditure")

    # Q8. Sustainability
    risk_mitigation_strategy_ids = fields.One2many('sparkit.riskmitigationstrategy', 'proposal_id',
        string="8a. What are the risks that the project may face and how will you avoid or address them?")
    engagement_strategy = fields.Text(string="8b. How will the community stay engaged in the project?")
    planned_meeting_ids = fields.One2many('sparkit.proposalplannedmeetings', 'proposal_id',
        string="8c. How often will the community meet, and what will be discussed?")
    community_leaders = fields.One2many('sparkit.proposalcommunityleaders', 'proposal_id', string="Community Leaders")

    # Q9. Transition Strategy
    resources_needed = fields.Text(string="9a. When your community’s project is operational, what kinds of additional training, resources and/or support will you need?")
    access_plan = fields.Text(string="9b. How do you plan to access these trainings, resources and support?")
    potential_partners = fields.Text(string="9c. What organizations or government partners can you reach out to?")
    learn = fields.Text(string="9d. How do you plan to learn from other communities in your area that have similar projects to yours? How will you engage with them? How will they help your project?")

    # Q10. Bylaws
    bylaw_ids = fields.One2many('sparkit.communitybylaws', 'proposal_id', string="Bylaws")

    @api.multi
    @api.depends('project_id')
    def _get_name(self):
        for r in self:
            if r.project_id:
                r.name = r.project_id.name + ' - '  + "Proposal"

class ProposalPME(models.Model):
    _name = 'sparkit.proposalpme'
    _rec_name = 'goal'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    goal = fields.Char(string="Goal", help="Overall, what is trying to be achieved?")
    metric = fields.Char(string="Metric",
        help="What do you need to measure to achieve this goal?")
    current_number = fields.Float(string="Current Number",
        help="What is the current number before project imlpementation?")
    target_month6 = fields.Float(string="Target - 6 Months PI",
        help="What does the community realistically think the target number will be 6 months post implementation?")
    target_month12 = fields.Float(string="Target - 12 Months PI",
        help="What does the community realistically think the target number will be 12 months post implementation?")
    target_month18 = fields.Float(string="Target - 18 months PI",
        help="What does the community realistically think the target number will be 18 months post implementation?")
    target_month24 = fields.Float(string="Target - 24 months PI",
        help="What does the community realistically think the target number will be 24 months post implementation?")

    #Action Plan
    collection_plan = fields.Text(string="How will this metric be collected?")
    collection_frequency = fields.Char(string="How often will this metric be gathered?")
    collection_resources = fields.Text(string="What inputs/resources are needed to collect this metric?")
    responsible = fields.Text(string="Who will be responsible for collecting this metric?",
        help="Please enter Name and Gender (M or F).")

class ProposalActivities(models.Model):
    _name = 'sparkit.proposalactivities'
    _rec_name = 'activity'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    activity = fields.Char(string="Step/Activity")
    inputs = fields.Text(string="Inputs")
    responsible = fields.Text(string="Person(s) Responsible",
        help="Please enter Name and Gender (M or F).")
    time_frame = fields.Char(string="Time Frame")

class ProposalBudget(models.Model):
    _name = 'sparkit.proposalbudget'
    _inherit = "sparkit.projectbudgetitem"

    responsible = fields.Text(string="Who is the person(s) responsible for purchasing the item?",
        help="Please enter Name and Gender (M or F).")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")
    community_id = fields.Many2one(related='proposal_id.community_id', store=True,)

class OperationalActivities(models.Model):
    _name = 'sparkit.operationalactivities'
    _rec_name = 'activity'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community",)
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    activity = fields.Char(string="Step/Activity")
    inputs = fields.Text(string="Inputs")
    responsible = fields.Text(string="Person(s) Responsible",
        help="Please enter Name and Gender (M or F).")
    time_frame = fields.Char(string="Time Frame")

class OperationalBudgetIncome(models.Model):
    _name = 'sparkit.operationalprofit'

    name = fields.Char(related='budget_item_id.name')

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    budget_item_id = fields.Many2one('sparkit.budgetitems', string="Item")
    unit = fields.Char(string="Unit Type", related='budget_item_id.unit', readonly=True, store=True)
    unit_number = fields.Float(string="Unit Number")
    unit_income = fields.Float(string="Unit Income")
    total_income = fields.Float(string="Total Income", readonly=True, compute='_get_total_income')
    responsible = fields.Char(string="Who will manage the money?", help="Please enter Name and Gender (M or F).")
    cash_storage = fields.Char(string="Where will it be stored?")

    @api.depends('unit_number', 'unit_income')
    def _get_total_income(self):
        for r in self:
            r.total_income = r.unit_number * r.unit_income


class OperationalBudgetExpenditure(models.Model):
    _name = 'sparkit.operationalexpenditure'

    name = fields.Char(related='budget_item_id.name')

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    budget_item_id = fields.Many2one('sparkit.budgetitems', string="Item")
    unit = fields.Char(string="Unit Type", related='budget_item_id.unit', readonly=True, store=True)
    unit_number = fields.Float(string="Unit Number")
    unit_cost = fields.Float(string="Unit Cost")
    total_cost = fields.Float(string="Total Cost", readonly=True, compute='_get_total_cost')
    responsible = fields.Char(string="Who is responsible for making payment?", help="Please enter Name and Gender (M or F).")

    @api.depends('unit_number', 'unit_cost')
    def _get_total_cost(self):
        for r in self:
            r.total_cost = r.unit_number * r.unit_cost

class RiskMitigationStrategy(models.Model):
    _name = 'sparkit.riskmitigationstrategy'
    _rec_name = 'risk'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    risk = fields.Text(string="Risk")
    mitigation_strategy = fields.Text(string="Mitigation Strategy")

class ProposalPlannedMeetings(models.Model):
    _name = 'sparkit.proposalplannedmeetings'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    meeting_type = fields.Char(string="Mtg. Type")
    meeting_frequency = fields.Char(string="Mtg. Frequency")
    discussion_topics = fields.Char(string="Mtg. Discussion Topics")
    activities = fields.Char(string="Mtg. Activities")

class ProposalCommunityLeaders(models.Model):
    _name = 'sparkit.proposalcommunityleaders'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    name = fields.Char(string="Position")
    responsibilities = fields.Text(string="Responsibilities")
    leader_ids = fields.Many2many('res.partner', string="Name")

class CommunityBylaws(models.Model):
    _name = 'sparkit.communitybylaws'

    community_id = fields.Many2one('sparkit.community', related='proposal_id.community_id',
        store=True, string="Community")
    proposal_id = fields.Many2one('sparkit.communityproposal', string="Proposal")

    name = fields.Text(string="Bylaw")
    number = fields.Char(string="Number")
