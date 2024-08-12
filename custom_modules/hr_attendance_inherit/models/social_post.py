from odoo import models, fields, api
import requests
from datetime import datetime

class SocialPost(models.Model):
    _name = 'social.post'
    _description = 'Social Post'

    account_id = fields.Many2one('social.media.account', required=True)
    content = fields.Text(required=True)
    scheduled_time = fields.Datetime(required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('posted', 'Posted'),
    ], default='draft')

    def schedule_post(self):
        self.state = 'scheduled'
        # Logic to schedule post using cron jobs

    def post_now(self):
        account = self.account_id
        content = self.content
        if account.platform == 'twitter':
            self._post_to_twitter(account, content)
        elif account.platform == 'facebook':
            self._post_to_facebook(account, content)
        elif account.platform == 'instagram':
            self._post_to_instagram(account, content)
        elif account.platform == 'linkedin':
            self._post_to_linkedin(account, content)
        self.state = 'posted'

    def _post_to_twitter(self, account, content):
        url = 'https://api.twitter.com/2/tweets'
        headers = {
            'Authorization': f'Bearer {account.access_token}',
            'Content-Type': 'application/json'
        }
        data = {'text': content}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise Exception('Failed to post to Twitter')

    def _post_to_facebook(self, account, content):
        url = 'https://graph.facebook.com/me/feed'
        data = {'message': content, 'access_token': account.access_token}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception('Failed to post to Facebook')

    def _post_to_instagram(self, account, content):
        url = 'https://graph.instagram.com/me/media'
        data = {'caption': content, 'access_token': account.access_token}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception('Failed to post to Instagram')

    def _post_to_linkedin(self, account, content):
        url = 'https://api.linkedin.com/v2/shares'
        headers = {
            'Authorization': f'Bearer {account.access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'content': {
                'contentEntities': [{
                    'entityLocation': '',
                    'thumbnails': [{'resolvedUrl': ''}]
                }],
                'title': content
            },
            'distribution': {
                'linkedInDistributionTarget': {}
            },
            'owner': f'urn:li:person:{account.user_id}',
            'subject': 'Post Subject'
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise Exception('Failed to post to LinkedIn')

    @api.model
    def post_scheduled(self):
        posts = self.search([('state', '=', 'scheduled'), ('scheduled_time', '<=', datetime.now())])
        for post in posts:
            post.post_now()
