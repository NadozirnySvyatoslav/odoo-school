from datetime import datetime,timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HRHospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Visit model'
    name = fields.Char(readonly=True,default=lambda self:_('New'))
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        readonly=True,
        states={'draft': [('readonly', False)], 'done': [('readonly', True)]},
        required=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        states={'draft': [('readonly', False)], 'done': [('readonly', True)]},
        required=True,
    )
    diagnose_id = fields.Many2one(
        comodel_name='hr_hospital.diagnose',
        copy=False,
        readonly=True,
    )
    description = fields.Text("Notes")
    planned_date = fields.Datetime(
        readonly=True,
        states={'draft': [('readonly', False)], 'done': [('readonly', True)]},
        copy=False,
    )
    state = fields.Selection(
        required=True,
        default='draft',
        selection=[
          ('draft', 'Draft'),
          ('wait', 'Waiting'),
          ('need_confirm', 'Need confirmation'),
          ('done', 'Done'),
          ('canceled', 'Canceled'),
        ],
    )

    def _check_planned_date(self,date):
        """Check if planned date more than 15 minutes from existed record"""
        planned_date=datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        min_date = planned_date - timedelta( minutes=15)
        max_date = planned_date + timedelta( minutes=15)
        records=self.env["hr_hospital.visit"].search(['&','&',('planned_date','>',min_date,),('planned_date','<',max_date),('id','!=',self.id)])
        if records:
            raise UserError(_("Date and time already taken"))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name']=self.env['ir.sequence'].next_by_code('hospital_visits')
        if vals.get('planned_date'):
            self._check_planned_date(vals.get('planned_date'))
        res=super(HRHospitalVisit, self).create(vals)
        return res

    def write(self, vals):
        if vals.get('planned_date'):
            self._check_planned_date(vals.get('planned_date'))
        if self.state in ('need_confirm','done') and not self.diagnose_id:
            raise UserError(_("Cannot close record  without diagnose"))

        res=super(HRHospitalVisit, self).write(vals)
        return res


    def action_cancel(self):
        return self.write({'state': 'canceled'})

    def action_done(self):
        if self.doctor_id and self.doctor_id.is_intern:
            self.write({'state': 'need_confirm'})
        else:
            self.write({'state': 'done'})

    def action_confirm(self):
        return self.write({'state': 'done'})

    def action_ready(self):
        return self.write({'state': 'wait'})

    def unlink(self):
        if self.state in ('canceled','done') and self.diagnose_id:
            raise UserError(_("Cannot delete closed record"))
        return super().unlink()


    def set_diagnose(self):
        view_id = self.env.ref('hr_hospital.choose_diagnose_view_form').id
        return {
            'name': "Add diagnose",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr_hospital.choose_diagnose',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_doctor_id': self.doctor_id.id,
                'default_patient_id': self.patient_id.id,
                'default_date': self.planned_date,
                'default_visit_id': self.id,
            }
        }


    def select_doctor_wizard(self):
        view_id = self.env.ref('hr_hospital.select_doctor_view_form').id
        return {
            'name': "Select doctor",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr_hospital.select_doctor',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_visit_id': self.id,
            }
        }
