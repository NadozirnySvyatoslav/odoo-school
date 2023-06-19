# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HRHospitalDiagnose(models.Model):
    _name = 'hr_hospital.diagnose'
    _description = 'Diagnose model used for determine the health of patient'
    name = fields.Char(readonly=True, compute="_compute_name")
    date = fields.Date(readonly=True)
    doctor_id=fields.Many2one("hr_hospital.doctor",readonly=True)
    patient_id=fields.Many2one("hr_hospital.patient",readonly=True)
    disease_id=fields.Many2one("hr_hospital.disease")
    visit_id=fields.Many2one("hr_hospital.visit")
    description = fields.Text()

    api.depends('disease_id')
    def _compute_name(self):
        for record in self:
            if record.disease_id:
                record.name=record.disease_id.name
            else:
                record.name="No diagnose"
