from odoo import models, fields, api

class HrPayrollPayslip(models.Model):
    _name = 'hr.payroll.payslip'
    _description = 'Payroll Payslip'

    name = fields.Char(string='Payslip Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    salary = fields.Float(string='Salary', required=True)
    deductions = fields.Float(string='Deductions')
    net_salary = fields.Float(string='Net Salary', compute='_compute_net_salary', store=True)

    @api.depends('salary', 'deductions')
    def _compute_net_salary(self):
        for record in self:
            record.net_salary = record.salary - record.deductions
