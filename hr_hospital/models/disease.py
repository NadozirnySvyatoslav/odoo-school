# -*- coding: utf-8 -*-

from odoo import models, fields


class HRHospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease model for description of diseases with name and description'
    name = fields.Char("Name",required=True)
    parent_id=fields.Many2one("hr_hospital.disease",index=True,ondelete="set null")
    description = fields.Text("Description")
