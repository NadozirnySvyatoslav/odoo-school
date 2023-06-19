# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api

class HRHospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient model'
    _inherit = "hr_hospital.person"
    birthday=fields.Date()
    age=fields.Integer(compute="_compute_age")

    passport_no=fields.Char(string="Passport number")
    contact_id=fields.Many2one('hr_hospital.contact_person','Personal contact')
    doctor_id=fields.Many2one('hr_hospital.doctor','Personal doctor')
    doctor_change_history_ids=fields.One2many('hr_hospital.doctor_change_history', 'patient_id', readonly=True)
    @api.depends('birthday')
    def _compute_age(self):
        for patient in self:
            if not patient.birthday:
                patient.age=0
            else:
                current_date=datetime.now()
                patient.age=current_date.year - patient.birthday.year

    def _update_history(self,doctor_id):
        data={
              "doctor_id":doctor_id,
              "patient_id":self.id,
              "date":datetime.now().isoformat(),
            }
        self.doctor_change_history_ids.create(data)


    def write(self,vals):
        if vals.get("doctor_id"):
            if self.doctor_id:
                if vals.get("doctor_id")!=self.doctor_id.id:
                    self._update_history(vals.get("doctor_id"))
            else:
                self._update_history(vals.get("doctor_id"))
        res=super(HRHospitalPatient, self).write(vals)
        return res
