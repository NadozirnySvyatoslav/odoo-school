from datetime import datetime
from odoo import models, fields, api


class HRHospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient model'
    _inherit = "hr_hospital.person"

    birthday = fields.Date()
    age = fields.Integer(compute="_compute_age")

    passport_no = fields.Char(string="Passport number")
    contact_id = fields.Many2one(comodel_name='hr_hospital.contact_person', string='Personal contact')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Personal doctor')
    doctor_change_history_ids = fields.One2many(comodel_name='hr_hospital.doctor_change_history',
                                                inverse_name='patient_id', readonly=True)

    @api.depends('birthday')
    def _compute_age(self):
        for patient in self:
            if not patient.birthday:
                patient.age = 0
            else:
                current_date = datetime.now()
                patient.age = current_date.year - patient.birthday.year

    def update_history(self, doctor_id):
        self.ensure_one()
        data = {
            "doctor_id": doctor_id.id,
            "patient_id": self.id,
            "date": datetime.now().isoformat(),
        }
        self.doctor_change_history_ids.create(data)

    def write(self, vals):
        for obj in self:
            if vals.get("doctor_id"):
                if obj.doctor_id:
                    if vals.get("doctor_id") != obj.doctor_id.id:
                        obj.update_history(vals.get("doctor_id"))
                else:
                    obj.update_history(vals.get("doctor_id"))
        res = super(HRHospitalPatient, self).write(vals)
        return res

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
                'default_doctor_id': self.doctor_id.id,
                'default_patient_id': self.id,
            }
        }
