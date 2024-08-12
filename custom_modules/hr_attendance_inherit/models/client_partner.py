from odoo import models, fields, api

class ClientPartner(models.Model):
    _name = 'client.partner'
    _description = 'Client and Partner Information'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    interaction_ids = fields.One2many('client.partner.interaction', 'client_partner_id', string='Interactions')

class ClientPartnerInteraction(models.Model):
    _name = 'client.partner.interaction'
    _description = 'Client and Partner Interaction History'

    client_partner_id = fields.Many2one('client.partner', string='Client/Partner', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    interaction_type = fields.Selection([
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    ], string='Interaction Type', required=True)
    notes = fields.Text(string='Notes')
