# -*- coding: utf-8 -*-

from odoo import models, fields


class HRHospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient model'

    name = fields.Char("Patient's name")
    description = fields.Text("Notes")
