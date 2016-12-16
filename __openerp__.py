# -*- coding: utf-8 -*-
{
    'name': "SparKit",

    'summary': """
         The Programatic Management Module of Spark's Model (the FCAP),
         including community management, financial accountability
         and facilitator oversight
    """,

    'description': """
    	This module has been specified and developed by Spark Microgrants for its
    	internal programatic management system - and for sharing with partner
    	organisations who wish to roll out the Facilitated Collective
    	Action Process (FCAP). This includes
			- Spark FCAP workflows
			- Government Partner CRM
			- Community Visit Tracker
			- All data collection tools
    """,

    'author': "Spark MicroGrants",
    'website': "http://www.sparkmicrogrants.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Application',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        #Security + Access Rules
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        #Custom Backend UI
        'views.xml',
    	#SparkIt Views
        'views/templates.xml',
        'views/communities.xml',
        'views/visit_report_form_base.xml',
        'views/transition_strategy.xml',
        'views/scouting_form.xml',
        'views/fcap_map.xml',
        'views/spark_projects.xml',
        'views/independent_projects.xml',
        'views/project_categories.xml',
        'views/savings_groups.xml',
        'views/ongoing_community_assesment.xml',
        'views/pillar_assessment.xml',
        'views/partnerships.xml',
        'views/pilots.xml',
        'views/communityproposal.xml',
        'views/country.xml',
        'views/res_partner_view.xml',
        #SparkIt Menu
        'views/sparkit_menu.xml',
        #Default/preloaded Data
        'data/scouted_community_sequences.xml',
        'data/partnered_community_sequences.xml',
        'data/visit_report_forms_sequences.xml',
        'data/savings_group_sequences.xml',
        'data/default_project_categories.xml',
        'data/default_biggest_concerns.xml',
        'data/default_crosssector_items.xml',
        'data/default_crosssector_animals.xml',
        'data/default_crosssector_illnesses.xml',
        'data/sparkit.projectsubcategory.csv',
        'data/default_trainings.xml',
        'data/default_FcapMap.xml',
        'data/sparkit.grouptracking.csv',
    	'data/sparkit.biggestconcernsubcategory.csv',
        'data/sparkit.fcapstep.csv',
        'data/sparkit.fcapactivity.csv',
        'data/default_workflow_configuration.xml',
        #workflows
        'views/community_workflow.xml',
    ],

    'qweb': [
        'static/src/xml/*.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}
