from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HRHospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Visit model'

    name = fields.Char(readonly=True, default=lambda self: _('New'))
    doctor_id = fields.Many2one(
        readonly=False,
        comodel_name='hr_hospital.doctor',
        states={'draft': [('readonly', False)], 'done': [('readonly', True)]},
        required=True,
    )
    patient_id = fields.Many2one(
        readonly=False,
        comodel_name='hr_hospital.patient',
        states={'draft': [('readonly', False)], 'done': [('readonly', True), ('required', True)]},
    )
    diagnose_id = fields.Many2one(
        readonly=True,
        comodel_name='hr_hospital.diagnose',
        copy=False,
    )
    description = fields.Text("Notes")
    planned_date = fields.Datetime(
        readonly=False,
        states={'draft': [('readonly', False)], 'done': [('readonly', True)]},
        copy=False,
    )
    state = fields.Selection(
        string="Status",
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

    analyses_ids = fields.One2many(comodel_name="hr_hospital.analysis", inverse_name="visit_id")

    def _check_date(self, rec_id, planned_date, doctor_id):
        min_date = planned_date - timedelta(minutes=15)
        max_date = planned_date + timedelta(minutes=15)
        return self.env["hr_hospital.visit"].search(
            ['&', '&', ('planned_date', '>', min_date,), ('planned_date', '<', max_date), ('id', '!=', rec_id),
             ('doctor_id', '=', doctor_id)])

    @api.constrains("planned_date")
    def _constrains_planned_date(self):
        for record in self:
            """Check if planned date more than 15 minutes from existed record"""
            records = self._check_date(record.id, record.planned_date, record.doctor_id.id)
            if records:
                raise ValidationError(_("Date and time already taken"))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital_visits')
        return super(HRHospitalVisit, self).create(vals)

    def write(self, vals):
        for obj in self:
            if obj.state in ['need_confirm', 'done'] and not obj.diagnose_id:
                raise UserError(_("Cannot close record  without diagnose"))
        return super(HRHospitalVisit, self).write(vals)

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
        if self.state in ('canceled', 'done') and self.diagnose_id:
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
