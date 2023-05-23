from odoo import models, fields, api
from odoo.exceptions import UserError


class z_popup(models.Model):
    _name = 'z_popup.z_popup'
    _description = 'z_popup.z_popup'

    name = fields.Char(string="Student")
    email = fields.Char(string="Email")
    registration_no = fields.Char(string="Registration No.")
    registered_date = fields.Date(string="Registration Date")

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            student = self.env['z_popup.student'].search([('name', '=', self.name)], limit=1)
            if student:
                self.email = student.email
            else:
                self.email = ''


    @api.constrains('email')
    def _check_unique_email(self):
        for record in self:
            if record.email:
                existing_registration = self.env['z_popup.z_popup'].search([('email', '=', record.email)])
                existing_student = self.env['z_popup.student'].search([('email', '=', record.email)])

                if existing_registration and record.id != existing_registration[0].id:
                    raise UserError("Email '%s' already exists in the registration table." % record.email)

                if not existing_student:
                    self.env['z_popup.student'].create({'name': record.name, 'email': record.email})


#     @api.depends('name')
#     def _compute_email(self):
#         for record in self:
#             if record.name:
#                 student = self.env['z_popup.student'].search([('name', '=', record.name)], limit=1)
#                 if student:
#                     record.email = student.email
#                 else:
#                     record.email = ''

#     def _inverse_email(self):
#         for record in self:
#             if record.name and record.email:
#                 student = self.env['z_popup.student'].search([('name', '=', record.name)], limit=1)
#                 if student:
#                     student.email = record.email
#                 else:
#                     self.env['z_popup.student'].create({'name': record.name, 'email': record.email})
