from datetime import datetime, timedelta
from odoo import models, fields
import logging

logger = logging.getLogger(__name__)


class DoctorVisit(models.TransientModel):
    _name = 'hr_hospital.doctor.visit'
    _description = 'Doctor visits planing Wizard'
    doctor_id = fields.Many2one(comodel_name="hr_hospital.doctor", required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    visit_start_hour = fields.Integer(required=True,default=9)
    visit_end_hour = fields.Integer(required=True,default=18)

    def action_set(self):
        self.ensure_one()
        date_start = datetime.combine(self.date_start,datetime.min.time())
        date_end = datetime.combine(self.date_end,datetime.min.time()) + timedelta(hours=self.visit_end_hour)

        while date_start < date_end:
            datetime_start = date_start + timedelta(hours=self.visit_start_hour)
            datetime_end = date_start + timedelta(hours=self.visit_end_hour)

            while datetime_start < datetime_end:
                logger.info(f"======== start {datetime_start}")
                visit_model = self.env["hr_hospital.visit"]
                records = visit_model._check_date(None, datetime_start, self.doctor_id.id)

                if not records:
                    visit_model.create({
                        'name': 'New',
                        'doctor_id': self.doctor_id.id,
                        'planned_date': datetime_start
                    })
                datetime_start+= timedelta(minutes=15)
            date_start += timedelta(days=1)
