from odoo import models, fields, api

class EmailMarketing(models.Model):
    _name = 'email.marketing'
    _description = 'Email Marketing'

    name = fields.Char(string='Campaign Name', required=True)
    subject = fields.Char(string='Subject', required=True)
    body = fields.Html(string='Email Body', required=True)
    recipient_ids = fields.Many2many('res.partner', string='Recipients')
    scheduled_date = fields.Datetime(string='Scheduled Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent')
    ], default='draft', string='Status')

    def action_schedule(self):
        self.write({'state': 'scheduled'})

    def action_send(self):
        # Implement the email sending logic
        self.write({'state': 'sent'})
