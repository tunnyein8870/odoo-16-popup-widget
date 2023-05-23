# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class z_popup(models.Model):
    _name = 'z_popup.z_popup'
    _description = 'z_popup.z_popup'

    a_field = fields.Char(string="Student")
    email = fields.Char(
        string="Email", compute="_compute_email", inverse="_inverse_email")
    registration_no = fields.Char(string="Registration No.")
    registered_date = fields.Date(string="Registration Date")

    @api.depends('a_field')
    def _compute_email(self):
        for record in self:
            if record.a_field:
                student = self.env['z_popup.student'].search(
                    [('name', '=', record.a_field)])
                record.email = student.email
            else:
                record.email = ''

    def _inverse_email(self):
            for record in self:
                # find student name in z_popup.student
                student = self.env['z_popup.student'].search(
                    [('name', '=', record.a_field)])
                # if student exists
                if student:
                    # When the student exists, it needs to add validation
                    student_email = student.email
                    self_email = record.email
                    print("=====student email", student.email)
                    print("===========record email", record.email)
                    student.write({'email': record.email})
                # if student not exists
                else:
                    self.env['z_popup.student'].create({'name': record.a_field, 'email': record.email})

# Email write without validation
 # def _inverse_email(self):
    #     for record in self:
    #         student = self.env['z_popup.student'].search(
    #             [('name', '=', record.a_field)])
    #         if student:
    #                 student.write({'email': record.email})
    #         else:
    #             self.env['z_popup.student'].create({'name': record.a_field, 'email': record.email})

# def _inverse_email(self):
#         for record in self:
#             if record.a_field and record.email:
#                 student = self.env['z_popup.student'].search([('name', '=', record.a_field)])
#                 if student:
#                     if student.email != record.email:
#                         existing_student = self.env['z_popup.student'].search([('email', '=', record.email)])
#                         if existing_student:
#                             raise UserError("Email already exists. Please input another email.")
#                         else:
#                             student.email = record.email
#                     else:
#                         student.email = record.email
#                 else:
#                     existing_student = self.env['z_popup.student'].search([('email', '=', record.email)])
#                     if existing_student:
#                         raise UserError("Email already exists. Please input another email.")
#                     else:
#                         self.env['z_popup.student'].create({'name': record.a_field, 'email': record.email})