from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HRHospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor model'
    _inherit = "hr_hospital.person"

    speciality = fields.Char()
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    intern_ids = fields.One2many(comodel_name='hr_hospital.doctor', inverse_name="mentor_id")

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

    def action_add_visit(self):
        view_id = self.env.ref('hr_hospital.hospital_visit_action_view_form').id
        return {
            'name': "Add visit",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr_hospital.visit',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            }
        }
