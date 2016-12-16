# -*- coding: utf-8 -*-

from openerp import models, fields, api

# TODO: Add in Learnings section/final review and approvals

class Pilot(models.Model):
    _name = 'sparkit.pilot'

    name = fields.Char(string="Name")
    date_started = fields.Date(string="Pilot Start Date")
    date_ended = fields.Date(string="Pilot End Date")
    description = fields.Text(string="Description")
    community_ids = fields.Many2many('sparkit.community', string="Communities",
        domain=[('is_partnered', '=', True)])

    #R&L Committee
    is_approved = fields.Boolean(string="Approved by Learning Committee?", default=False)
    proposal_submission_date = fields.Date(string="Proposal Submission Date")
    proposed_start_date = fields.Date(string="Proposed Start Date")

    #Indicators
    is_using_preset_indicators = fields.Boolean(string="Custimized Indicator Fields?", default=False,
        help="Check this box to hide indicators 1-10 if pilot will be using custom indicators")

    #FLEXIBLE Indicators That Updates Will Be Collected On
    indicator1 = fields.Char(string="Indicator 1")
    indicator2 = fields.Char(string="Indicator 2")
    indicator3 = fields.Char(string="Indicator 3")
    indicator4 = fields.Char(string="Indicator 4")
    indicator5 = fields.Char(string="Indicator 5")
    indicator6 = fields.Char(string="Indicator 6")
    indicator7 = fields.Char(string="Indicator 7")
    indicator8 = fields.Char(string="Indicator 8")
    indicator9 = fields.Char(string="Indicator 9")
    indicator10 = fields.Char(string="Indicator 10")

    #Pilot Research & Learning Proposal
    leading_activity = fields.Many2many('res.users',
        string="""1. Who is leading this learning activity? Please list up to two names,
        and any other pilots they are involved in.""")
    supporting_activity = fields.Text(
        string="2. Who is supporting this learning activity? What other pilots, if any, are they involved in")
    learning_description = fields.Text(
        string="3. Please briefly describe your learning activity topic and why you chose it?")
    learning_contribution = fields.Text(
        string="""4. How will your learning contribute to the FCAP, to Spark’s work with communities,
        Spark’s mission and vision, or to the organization overall?""")
    key_questions = fields.Text(
        string="5. Please describe your learning goals or key questions.")
    key_outputs = fields.Text(
        string="""6. Please describe the anticipated outputs of your learning activity.
        If you already have a draft or version of this output, please note it below, and submit a copy with this proposal""")
    activities = fields.One2many('sparkit.pilotactivities', 'pilot_id')
    sharing = fields.One2many('sparkit.pilotsharing', 'pilot_id')
    success = fields.Text(string="9. What does success look like for your learning activity?")
    risks = fields.One2many('sparkit.pilotrisks', 'pilot_id')
    spark_support = fields.Text(string="11. What support would you like from the Spark team?")
    lc_support = fields.Text(string="12. What support would you like from the Learning Committee?")

    #Pilot Updates
    pilot_update_ids = fields.One2many('sparkit.pilotupdate', 'pilot_id')


class PilotActivities(models.Model):
    _name = 'sparkit.pilotactivities'

    pilot_id = fields.Many2one('sparkit.pilot', string="Pilot")
    name = fields.Char(string="Activity")
    responsible = fields.Many2many('res.users', string="Person(s) Responsible")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    location = fields.Char(string="Location")
    resources = fields.Text(string="Resources Needed")
    data = fields.Text(string="Information/Data Collected")


class PilotSharing(models.Model):
    _name = 'sparkit.pilotsharing'

    pilot_id = fields.Many2one('sparkit.pilot', string="Pilot")
    name = fields.Char(string="Sharing Opportunity")
    responsible = fields.Many2many('res.users', string="Person(s) Responsible")
    sharing_format = fields.Text(string="Format (ex.one-pager, presentation, discussion, etc.)")
    sharing_deadline = fields.Date(string="Sharing Deadline")

class PilotRiskMitigation(models.Model):
    _name = 'sparkit.pilotrisks'

    pilot_id = fields.Many2one('sparkit.pilot', string="Pilot")
    name = fields.Text(string="Risk(s) Associated with Activity")
    plan = fields.Text(string="Plan(s) to Address Risks(s)")


class PilotUpdate(models.Model):
    _name = 'sparkit.pilotupdate'

    name = fields.Char(compute='_get_name')
    date = fields.Date(string="Date")
    pilot_id = fields.Many2one('sparkit.pilot', string="Pilot")
    pilot_name = fields.Char(related='pilot_id.name')
    community_id = fields.Many2one('sparkit.community', string="Community")
    community_name = fields.Char(related='community_id.name', store=True)
    facilitator_id = fields.Many2one('res.users', string="Facilitator")

    #Indicators (only shown if preset indicators is True in XML)
    indicator1_name = fields.Char(related='pilot_id.indicator1', string="", readonly=True)
    indicator1 = fields.Char()
    indicator2_name = fields.Char(related='pilot_id.indicator2', string="", readonly=True)
    indicator2 = fields.Char()
    indicator3_name = fields.Char(related='pilot_id.indicator3', string="", readonly=True)
    indicator3 = fields.Char()
    indicator4_name = fields.Char(related='pilot_id.indicator4', string="", readonly=True)
    indicator4 = fields.Char()
    indicator5_name = fields.Char(related='pilot_id.indicator5', string="", readonly=True)
    indicator5 = fields.Char()
    indicator6_name = fields.Char(related='pilot_id.indicator6', string="", readonly=True)
    indicator6 = fields.Char()
    indicator7_name = fields.Char(related='pilot_id.indicator7', string="", readonly=True)
    indicator7 = fields.Char()
    indicator8_name = fields.Char(related='pilot_id.indicator8', string="", readonly=True)
    indicator8 = fields.Char()
    indicator9_name = fields.Char(related='pilot_id.indicator9', string="", readonly=True)
    indicator9 = fields.Char()
    indicator10_name = fields.Char(related='pilot_id.indicator10', string="", readonly=True)
    indicator10 = fields.Char()

    challenges = fields.Text(string="Any challenge(s) related to the pilot?")
    successes = fields.Text(string="Any success(es) related to the pilot?")
    comments = fields.Text(string="Other Comments")

    @api.multi
    @api.depends('community_id', 'pilot_id', 'date')
    def _get_name(self):
        for r in self:
            if r.pilot_id:
                r.name = str(r.pilot_name) + ' - ' + str(r.community_name) + ': ' + str(r.date)
