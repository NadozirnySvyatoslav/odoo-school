from odoo import models, fields

class HRHospitalDoctorChangeHistory(models.Model):
    _name = 'hr_hospital.doctor_change_history'
    _description = 'Visit model'
    doctor_id = fields.Many2one(
        comodel_name="hr_hospital.doctor",
        readonly=True,
    )
    patient_id = fields.Many2one(
        readonly=True,
        comodel_name='hr_hospital.patient',
    )
    date = fields.Date(readonly=True)
