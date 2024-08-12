from odoo import models, fields

class SocialMediaAccount(models.Model):
    _name = 'social.media.account'
    _description = 'Social Media Account'

    name = fields.Char(required=True)
    platform = fields.Selection([
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
    ], required=True)
    access_token = fields.Char(required=True)
    api_url = fields.Char()  # API URL for posting and fetching data
    user_id = fields.Char()  # User ID for social platforms
