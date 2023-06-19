from odoo import fields, models


class ChooseDiagnose(models.TransientModel):
    _name = 'hr_hospital.choose_diagnose'
    _description = 'Diagnose Selection Wizard'
    date = fields.Date(readonly=True, required=True)
    doctor_id=fields.Many2one("hr_hospital.doctor",readonly=True, required=True)
    patient_id=fields.Many2one("hr_hospital.patient",readonly=True, required=True)
    disease_id=fields.Many2one("hr_hospital.disease", required=True)
    visit_id=fields.Many2one("hr_hospital.visit", required=True)
    description = fields.Text()

    def action_set(self):
        Diagnose=self.env["hr_hospital.diagnose"]
        Visit=self.env["hr_hospital.visit"]
        visit=Visit.search([("id",'=',self.visit_id.id)])
        diagnose=Diagnose.search([("visit_id",'=',self.visit_id.id)])
        diagnose.unlink()
        data={
          "date": self.date,
          "doctor_id": self.doctor_id.id,
          "patient_id": self.patient_id.id,
          "disease_id": self.disease_id.id,
          "visit_id": self.visit_id.id,
          "description": self.description,
        }
        diagnose=Diagnose.create(data)
        visit.write({"diagnose_id":diagnose.id})
