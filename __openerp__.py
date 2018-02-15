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
    	Action Process (FCAP).
    """,

    'author': "Spark MicroGrants",
    'website': "http://www.sparkmicrogrants.org",

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
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        #Custom Backend UI
        'views.xml',
    	#SparkIt Views
        'views/community_views.xml',
        'views/visit_report_form_views.xml',
        'views/transition_strategy_views.xml',
        'views/scouting_form_views.xml',
        'views/fcap_map_views.xml',
        'views/spark_project_views.xml',
        'views/independent_project_views.xml',
        'views/project_category_views.xml',
        'views/savings_group_views.xml',
        'views/ongoing_community_assesment_views.xml',
        'views/partnership_views.xml',
        'views/communityproposal.xml',
        'views/res_country_views.xml',
        'views/res_partner_views.xml',
        'views/community_workflow_parameters_views.xml',
        'views/res_currency_view.xml',
        'views/res_users_views.xml',
        'views/cmty_name_change_wizard.xml',
        'views/programreview_views.xml',
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
        'data/default_FcapMap.xml',
        'data/sparkit.grouptracking.csv',
    	'data/sparkit.biggestconcernsubcategory.csv',
        'data/sparkit.fcapstep.csv',
        'data/sparkit.fcapactivity.csv',
        'data/default_workflow_configuration.xml',
        #workflows
        'views/community_workflow.xml',

        # Disabling VRF Workflow for Imports
        # 'views/visit_report_form_workflow.xml',

    ],

    'qweb': [
        'static/src/xml/*.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}
