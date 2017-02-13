# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import ValidationError, Warning


    #---------------------------------------------------
	#      FCAP   Workflow Parameters Class           |
	#---------------------------------------------------

class CommunityWorkflowParameters(models.Model):
    _name = 'sparkit.communityworkflowparameters'

    name = fields.Char(string="Name")

    # Community Identification -> Introductions
    is_oca1_completed = fields.Boolean(string="OCA 1 Required")

    # Partnership to Community Building
    is_partnership_hh_requirement_met = fields.Boolean(string="Minimum Percent of Households Signing Partnership Agreement Required?")
    # Breakpoint - default = False
    using_hh_breakpoint = fields.Boolean(string="Use Breakpoint?", help="Only check this button if the workflow configuration will be using a household breakpoint.")
    # Minimum number of households that signed partnership agreement
    min_percent_hh_partnership = fields.Float(string="Minimum Percent of Total Households in the Community That Must Sign Partnership Agreement")
    # Partnership -> Community Building
    #T his variable defines the 'breakpoint' for % of community that signed the partnership agreement,
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
    is_cmty_leaders_entered = fields.Boolean(string="Leaders Required to be Entered?")
    num_leaders_requirement = fields.Boolean(string="Number of Elected Leaders Requirement?")
    leaders_gender_requirement = fields.Boolean(string="Gender of Elected Leaders Requirement?")
    sms_registration_completed = fields.Boolean(string="SMS Registration Required?")
    communitybldg_min_elected_leaders = fields.Integer(string="Minimum Number of Elected Leaders")
    communitybldg_max_elected_leaders = fields.Integer(string="Maximum Number of Elected Leaders")
    communtiybldg_min_percent_female = fields.Float(string="Minimum Percent Female Leaders")

    # Goals -> Pathways
    min_goals_brainstormed = fields.Integer(string="Minimum Number of Goals Brainstormed")
    min_pathways_brainstormed = fields.Integer(string="Minimum Number of Pathways Brainstormed")

    # Pathways -> Implementation Action Plan
    is_oca2_completed = fields.Boolean(string="OCA2 Required?")
    did_ta_recruitment_begin = fields.Boolean(string="TA Recruitment Required?")
    did_bank_opening_begin = fields.Boolean(string="Opening Bank Account Required?")
    did_government_registration_begin = fields.Boolean(string="Government Registration Required?")
    pm_approved_goal_setting = fields.Boolean(string="Manager Approved Goal Setting Required?")

    # Implementation Plan to Operational Plan
    cmty_facilitators_identified = fields.Boolean(string="Community Facilitators Required?")

    # Proposal Finalization -> Imp: Grant Agreement
    is_bank_account_created = fields.Boolean(string="Bank Account Required?")
    has_pm_approved_proposal = fields.Boolean(string="PM Required to Approve Proposal?")
    is_oca3_completed = fields.Boolean(string="OCA3 Required?")
    cmty_registered_with_govt = fields.Boolean(string="Community Required to be Registered with Local Government?")

    # Implementation Grant Agreement -> First Disbursement
    is_receipt_book_received = fields.Boolean(string="Receipt Book Received Required?")
    is_disbursement_book_received = fields.Boolean(string="Disbursement Book Received Required?")
    is_cashbook_received = fields.Boolean(string="Cashbook Received Required?")
    min_pg_signed_agreement = fields.Boolean(string="Minimum Percent of Planning Group Signing Grant Agreement Required?")
    percent_pg_signed_grantagreement = fields.Float(string="Percent of Planning Group That Must Sign Grant Agreement")

    # Implementation: Transition Strategy -> Post Implementation 1
    is_project_quality_approved_ta = fields.Boolean(string="Project Quality Approved by TA Required?")
    is_imp_action_plan_completed = fields.Boolean(string="Completed Implementation Action Plan Verfied by TA Required?")
    is_transition_strategy_completed = fields.Boolean(string="Transition Strategy Completed Required")
    cmty_facilitation_training = fields.Boolean(string = "Community Facilitation Training Required?")
    field_audit_passed = fields.Boolean(string="Field Audit Required?")
    cmty_report1_submitted = fields.Boolean(string="Community Report 1 Submitted Required?")

    # PI1 to PI 2
    is_oca4_completed = fields.Boolean(string="OCA 4 Required?")
    is_oca5_completed = fields.Boolean(string="OCA 5 Required?")

    # PI2 to PI 3
    cmty_report2_submitted = fields.Boolean(string="Community Report Required?")
    is_oca6_completed = fields.Boolean(string="OCA 6 Required?")

    # PI3 to Graduation
    cmty_passed_field_audit_pi3 = fields.Boolean(string="Community Passed Field Audit Required?")
    cmty_report3_submitted = fields.Boolean(string="Community Report Required?")
    exit_agreement_uploaded = fields.Boolean(string="Exit Agreement Required?")
    exit_agreement_signed = fields.Boolean(string="Minimum Number Of Signatories on Exit Requirement Required?")
    percent_pg_signed_exitagreement = fields.Float(string="Percent of Planning Group That Must Sign Exit Agreement")
    is_oca7_completed = fields.Boolean(string="OCA 7 Required?")
    is_oca8_completed = fields.Boolean(string="OCA 8 Required?")
    exit_agreement_uploaded = fields.Boolean(string="Exit Agreement Required to be Uploaded?")

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

    @api.constrains('min_percent_hh_partnership')
    def _check_min_percent_hh_partnership(self):
        for r in self:
        	if r.min_percent_hh_partnership > 1:
        		raise ValidationError("Error: Must be less than 1")

    @api.constrains('percent_pg_signed_grantagreement')
    def _check_percent_pg_signed_grantagreement(self):
        for r in self:
        	if r.percent_pg_signed_grantagreement > 1:
        		raise ValidationError("Error: Must be less than 1")

    @api.constrains('percent_pg_signed_exitagreement')
    def _check_percent_pg_signed_exitagreement(self):
        for r in self:
        	if r.percent_pg_signed_exitagreement > 1:
        		raise ValidationError("Error: Must be less than 1")

    _sql_constraints = [
    #Unique Workfow
    ('name_unique',
    'UNIQUE(name)',
    "The community name must be unique"),
    ]
