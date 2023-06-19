# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HRHospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor model'
    _inherit = "hr_hospital.person"
    speciality = fields.Char()
    is_intern=fields.Boolean()
    mentor_id = fields.Many2one('hr_hospital.doctor')


    def _check_is_intern(self,mentor_id):
        mentor=self.env['hr_hospital.doctor'].search([('id','=',mentor_id)])
        if mentor.is_intern:
            raise UserError(_("Intern cannot be as a mentor"))

    @api.model
    def create(self, vals):
        if vals.get('mentor_id'):
            self._check_is_intern(vals.get('mentor_id'))
        res=super(HRHospitalDoctor, self).create(vals)
        return res

    def write(self, vals):
        if vals.get('mentor_id'):
            self._check_is_intern(vals.get('mentor_id'))
        res=super(HRHospitalDoctor, self).write(vals)
        return res
