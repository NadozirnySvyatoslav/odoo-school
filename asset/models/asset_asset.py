from odoo import models, fields


class Asset(models.Model):
    _name = 'asset.asset'
    _description = 'Asset model for device accounting'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", compute="_compute_name", readonly=True)
    employee_id = fields.Many2one('hr.employee', readonly=False, string='Assigned Employee')
    department_id = fields.Many2one('hr.department', readonly=False, string='Assigned Department')
    model_id = fields.Many2one('asset.model', string='Model', required=True)
    location = fields.Char('Location', required=True)
    number = fields.Char(string="Number")
    serial_no = fields.Char('Serial Number', copy=False, required=True)
    install_date = fields.Date('Installation Date')
    warranty_date = fields.Date('Warranty Expiration Date')

    def name_get(self):
        return [(tag.id, f"{tag.number}, {tag.model_id.name} [{tag.serial_no}] {tag.location}") for tag in self]
