from odoo import models, fields

class HRHospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Visit model'
    name = fields.Char()
    doctor_id = fields.Many2one('hr_hospital.doctor', string="Doctor", required=True, help="Doctor")
    patient_id = fields.Many2one('hr_hospital.patient', string="Patient", required=True, help="Patient")
    disease_id = fields.Many2one('hr_hospital.disease', string="Diagnose", help="Diagnose")
    description = fields.Text("Notes")
    planned_date = fields.Date( string='Planned date' )
    visited_date = fields.Date( string='Visited date' )
