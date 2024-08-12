from odoo import models, fields

class EmployeeCheckInDashboard(models.Model):
    _name = 'employee.checkin.dashboard'
    _description = 'Employee Check-In Dashboard'

    name = fields.Char(string="Name")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    check_in_status = fields.Selection([('pending', 'Pending'), ('completed', 'Completed')], string="Check-In Status")

    def mark_as_completed(self):
        self.check_in_status = 'completed'
