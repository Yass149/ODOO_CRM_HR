# File: custom_modules/hr_attendance_inherit/models/custom_journal_entry.py

from odoo import models, fields, api

class AuditLog(models.Model):
    _name = 'audit.log'
    _description = 'Audit Log'

    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users', string='User')
    entry_id = fields.Integer(string='Entry ID')
    description = fields.Text(string='Description')
    # Add more fields as needed


class CustomJournalEntry(models.Model):
    _name = 'custom.journal.entry'
    _description = 'Custom Journal Entry'

    account_id = fields.Many2one('custom.account', string='Account')
    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    debit = fields.Float(string='Debit')
    credit = fields.Float(string='Credit')
    description = fields.Char(string='Description')
    # Add more fields as needed

    @api.model
    def create(self, vals):
        new_entry = super(CustomJournalEntry, self).create(vals)
        self.env['audit.log'].create({
            'name': f'Journal Entry Created: {new_entry.name}',
            'user_id': self.env.user.id,
            'entry_id': new_entry.id,
            'description': 'New journal entry created',
        })
        return new_entry

    def write(self, vals):
        res = super(CustomJournalEntry, self).write(vals)
        for entry in self:
            self.env['audit.log'].create({
                'name': f'Journal Entry Updated: {entry.name}',
                'user_id': self.env.user.id,
                'entry_id': entry.id,
                'description': 'Journal entry updated',
            })
        return res
