from odoo import models


class HRHospitalContactPerson(models.Model):
    _name = 'hr_hospital.contact_person'
    _description = 'Personal contact model for patients who can helps'
    _inherit = "hr_hospital.person"
