from odoo import models, fields, api


class HRHospitalPerson(models.AbstractModel):
    _name = 'hr_hospital.person'
    _description = 'Abstract person model'

    name = fields.Char(readonly=True, compute='_compute_name')
    first_name = fields.Char(required=True)
    surname = fields.Char(required=True)
    email = fields.Char()
    phone = fields.Char()
    photo = fields.Image()
    sex = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    description = fields.Text(string="Notes")

    @api.depends('first_name', 'surname')
    def _compute_name(self):
        for person in self:
            person.name = f"{person.surname} {person.first_name}"
