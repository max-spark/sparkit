# -*- coding: utf-8 -*-

from openerp import models, fields, api

#Project Categories for Both Spark Projects and Independent Projects

class ProjectCategory(models.Model):
	_name = 'sparkit.projectcategory'

	name = fields.Char(string="Primary Project Category")
	subcategory_ids = fields.One2many('sparkit.projectsubcategory', 'category_id',
		string="Sub-Categories", ondelete='cascade')

class ProjectSubCategory(models.Model):
	_name = 'sparkit.projectsubcategory'

	name = fields.Char(string="Project SubCategory")
	category_id = fields.Many2one('sparkit.projectcategory', string="Category",
		ondelete='cascade')
