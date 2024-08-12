from odoo import models, fields, api
from datetime import datetime, timedelta

class Employee(models.Model):
    _inherit = 'hr.employee'

    can_work_remotely = fields.Boolean(string="Can Work Remotely")

    @api.model
    def send_check_in_reminders(self):
        employees = self.search([('work_email', '!=', False)])
        for employee in employees:
            # Send internal notification
            message = "This is a reminder to check in for the day."
            employee.message_post(
                body=message,
                subtype_xmlid='mail.mt_comment'
            )

            # Update employee dashboard or other records as needed

            # Example: Creating a new record in 'employee.checkin.dashboard'
            self.env['employee.checkin.dashboard'].create({
                'name': f'Check-In Reminder for {employee.name}',
                'employee_id': employee.id,
                'check_in_status': 'pending',
            })

            # Calculate nextcall datetime (for cron job)
            nextcall = datetime.now() + timedelta(hours=10)

            # Create or update ir.cron record
            cron_record = self.env['ir.cron'].search([('name', '=', 'Check-In Reminder')])
            if not cron_record:
                cron_record = self.env['ir.cron'].create({
                    'name': 'Check-In Reminder',
                    'model_id': self.env.ref('hr.model_hr_employee').id,
                    'state': 'code',
                    'code': 'model.send_check_in_reminders()',
                    'active': True,
                    'interval_number': 1,
                    'interval_type': 'days',
                    'numbercall': -1,
                    'doall': False,
                    'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                })
            else:
                cron_record.write({'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S')})
