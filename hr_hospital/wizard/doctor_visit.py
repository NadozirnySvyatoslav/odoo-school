from datetime import datetime, timedelta, timezone
from odoo import models, fields
from pytz import timezone, utc
import logging

logger = logging.getLogger(__name__)


class DoctorVisit(models.TransientModel):
    _name = 'hr_hospital.doctor.visit'
    _description = 'Doctor visits planing Wizard'
    doctor_id = fields.Many2one(comodel_name="hr_hospital.doctor", required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    visit_start_hour = fields.Integer(required=True, default=9)
    visit_end_hour = fields.Integer(required=True, default=18)

    def action_set(self):
        self.ensure_one()

        local_tz = timezone(self.env.user.tz or 'UTC')
        date_start = datetime.combine(self.date_start, datetime.min.time())
        date_end = datetime.combine(self.date_end, datetime.min.time()) + timedelta(hours=self.visit_end_hour)

        while date_start < date_end:
            datetime_start = date_start + timedelta(hours=self.visit_start_hour)
            datetime_end = date_start + timedelta(hours=self.visit_end_hour)

            while datetime_start < datetime_end:
                logger.info(f"======== start {datetime_start}")
                visit_model = self.env["hr_hospital.visit"]
                native_dt = datetime_start
                local_dt = local_tz.localize(native_dt, is_dst=None)
                utc_dt = local_dt.astimezone(utc)
                records = visit_model._check_date(None, utc_dt, self.doctor_id.id)

                if not records:
                    visit_model.create({
                        'name': 'New',
                        'doctor_id': self.doctor_id.id,
                        'planned_date': utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                    })
                datetime_start += timedelta(minutes=15)
            date_start += timedelta(days=1)
