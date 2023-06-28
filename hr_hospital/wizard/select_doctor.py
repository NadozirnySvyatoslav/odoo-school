from odoo import fields, models, _
from odoo.exceptions import UserError


class SelectDoctor(models.TransientModel):
    _name = 'hr_hospital.select_doctor'
    _description = 'Doctor Selection Wizard'
    doctor_id = fields.Many2one(comodel_name="hr_hospital.doctor", required=True)
    visit_ids = fields.Many2many(comodel_name="hr_hospital.visit", relation='select_doctor_rel', column1='select_id',
                                 column2='visit_id')

    def action_set(self):
        if not self.doctor_id.id:
            raise UserError(_("Need to choose doctor for update visits"))
        active_ids = self._context.get('active_ids', [])
        visits = self.env['hr_hospital.visit'].search([('id', 'in', active_ids)])
        visits.write({
            'doctor_id': self.doctor_id.id
        })
