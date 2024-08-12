from odoo import models, fields, api

class HrTraining(models.Model):
    _name = 'hr.training'
    _description = 'HR Training'

    name = fields.Char(string='Training Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Participants')

class HrTrainingSession(models.Model):
    _name = 'hr.training.session'
    _description = 'HR Training Session'

    name = fields.Char(string='Session Name', required=True)
    training_id = fields.Many2one('hr.training', string='Training', required=True)
    session_date = fields.Date(string='Session Date', required=True)
    instructor_id = fields.Many2one('hr.employee', string='Instructor')
    attendee_ids = fields.Many2many('hr.employee', string='Attendees')
