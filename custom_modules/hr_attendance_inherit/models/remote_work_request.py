from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RemoteWorkRequest(models.Model):
    _name = 'remote.work.request'
    _description = 'Remote Work Request'

    name = fields.Char(string='Request Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    latitude = fields.Float(string='Latitude', required=True)
    longitude = fields.Float(string='Longitude', required=True)
    radius = fields.Float(string='Radius (meters)', required=True)
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft', string='Status')

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'

