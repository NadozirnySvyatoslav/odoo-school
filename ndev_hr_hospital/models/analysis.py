from datetime import datetime
from odoo import models, fields, api

import logging

logger = logging.getLogger(__name__)


class HRHospitalAnalysisValue(models.Model):
    _name = 'hr_hospital.analysis.value'
    value = fields.Char(required=True)
    name = fields.Char()
    analysis_id = fields.Many2one(comodel_name="hr_hospital.analysis")


class HRHospitalAnalysis(models.Model):
    _name = 'hr_hospital.analysis'
    _description = 'Analysis model used for determine the health of patient'

    name = fields.Char(required=True)
    date = fields.Date()
    doctor_id = fields.Many2one(comodel_name="hr_hospital.doctor", readonly=True)
    patient_id = fields.Many2one(comodel_name="hr_hospital.patient", readonly=True)
    visit_id = fields.Many2one(comodel_name="hr_hospital.visit", readonly=True)
    value_ids = fields.One2many(comodel_name="hr_hospital.analysis.value", inverse_name="analysis_id", string="Values")

    @api.model
    def default_get(self, values):
        vals = super(HRHospitalAnalysis, self).default_get(values)
        vals["date"] = datetime.now()
        if self.env.context.get("default_doctor_id"):
            vals["doctor_id"] = self.env.context.get("default_doctor_id")
        if self.env.context.get("default_patient_id"):
            vals["patient_id"] = self.env.context.get("default_patient_id")

        return vals
