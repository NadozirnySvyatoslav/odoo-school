from odoo import models, fields


class AssetModel(models.Model):
    _name = 'asset.model'
    _description = 'Asset model model for device'

    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor')