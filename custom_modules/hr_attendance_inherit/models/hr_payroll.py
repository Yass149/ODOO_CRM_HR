# hr_attendance_inh/models/hr_payroll.py
from odoo import models, fields, api

class HRPayroll(models.Model):
    _name = 'hr.payroll'
    _description = 'Payroll'

    name = fields.Char(string='Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    salary_amount = fields.Float(string='Salary Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid')
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.payroll') or 'New'
        return super(HRPayroll, self).create(vals)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_pay(self):
        self.state = 'paid'
