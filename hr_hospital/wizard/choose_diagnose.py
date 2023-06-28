from odoo import fields, models


class ChooseDiagnose(models.TransientModel):
    _name = 'hr_hospital.choose_diagnose'
    _description = 'Diagnose Selection Wizard'

    date = fields.Date(readonly=True, required=True)
    doctor_id = fields.Many2one(comodel_name="hr_hospital.doctor", readonly=True, required=True)
    patient_id = fields.Many2one(comodel_name="hr_hospital.patient", readonly=True, required=True)
    disease_id = fields.Many2one(comodel_name="hr_hospital.disease", required=True)
    visit_id = fields.Many2one(comodel_name="hr_hospital.visit", required=True)
    description = fields.Text()

    def action_set(self):
        diagnose_model = self.env["hr_hospital.diagnose"]
        visit_model = self.env["hr_hospital.visit"]
        visit = visit_model.search([("id", '=', self.visit_id.id)])
        diagnose = diagnose_model.search([("visit_id", '=', self.visit_id.id)])
        diagnose.unlink()
        data = {
            "date": self.date,
            "doctor_id": self.doctor_id.id,
            "patient_id": self.patient_id.id,
            "disease_id": self.disease_id.id,
            "visit_id": self.visit_id.id,
            "description": self.description,
        }
        diagnose = diagnose_model.create(data)
        visit.write({"diagnose_id": diagnose.id})
