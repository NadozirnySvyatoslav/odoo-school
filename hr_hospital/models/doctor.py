# -*- coding: utf-8 -*-

from odoo import models, fields


class HRHospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor model'
    name = fields.Char("Doctor's Name")
    description = fields.Text("Notes")
