# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp import exceptions

class sparkit_cmty_name_change_wizard(models.TransientModel):
    _name = 'sparkit.cmty_name_change_wizard'

    community_ids = fields.Many2many('sparkit.community', string="Communities")
    new_name = fields.Char(string="Updated Name")

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        # else:
        self.community_ids.write({'name': self.new_name})
        return True

    @api.multi
    def do_reopen_form(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window',
                'res_model': self._name, # this model
                'res_id': self.id,  # the current wizard record
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'}
