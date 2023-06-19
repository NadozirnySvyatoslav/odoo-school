from odoo import fields, models, _
from odoo.exceptions import UserError

class SelectDoctor(models.TransientModel):
    _name = 'hr_hospital.select_doctor'
    _description = 'Doctor Selection Wizard'
    doctor_id=fields.Many2one("hr_hospital.doctor", required=True)
    visit_ids=fields.Many2many("hr_hospital.visit", 'select_doctor_rel', 'select_id', 'visit_id')

    def action_set(self):
        if not self.doctor_id.id:
            raise UserError(_("Need to choose doctor for update visits"))
        active_ids = self._context.get('active_ids', [])
        visits=self.env['hr_hospital.visit'].search([('id','in',active_ids)])
        for visit in visits:
            visit.write({
              'doctor_id': self.doctor_id.id
            })
