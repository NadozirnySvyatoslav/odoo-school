from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HRHospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor model'
    _inherit = "hr_hospital.person"

    speciality = fields.Char()
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor')

    @api.model
    def _check_is_intern(self, mentor_id):
        self.ensure_one()
        mentor = self.env['hr_hospital.doctor'].browse(mentor_id)
        if mentor.is_intern:
            raise ValidationError(_("Intern cannot be as a mentor"))
        if mentor.id == self.id:
            raise ValidationError(_("Doctor cannot be as a mentor for himself"))

    @api.model
    def create(self, vals):
        if vals.get('mentor_id'):
            self._check_is_intern(vals.get('mentor_id'))
        return super(HRHospitalDoctor, self).create(vals)

    def write(self, vals):
        for obj in self:
            if vals.get('mentor_id'):
                obj._check_is_intern(vals.get('mentor_id'))
        return super(HRHospitalDoctor, self).write(vals)
