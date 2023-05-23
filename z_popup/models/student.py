# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class student(models.Model):
    _name = 'z_popup.student'

    name = fields.Char()
    email = fields.Char()
    
    @api.model
    # record_id is obtained via rpc in js
    def get_name(self, record_id):
        record = self.browse(record_id)

        return {
            'name': record.name,
            'email': record.email,
        }
    
    
        