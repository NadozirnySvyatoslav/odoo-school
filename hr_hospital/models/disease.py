# -*- coding: utf-8 -*-

from odoo import models, fields


class HRHospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease model'
    name = fields.Char("Name")
    description = fields.Text("Description")
