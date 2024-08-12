from odoo import models, fields, api
import requests

class SocialFeed(models.Model):
    _name = 'social.feed'
    _description = 'Social Feed'

    account_id = fields.Many2one('social.media.account', required=True)
    post_id = fields.Char(required=True)
    content = fields.Text()
    timestamp = fields.Datetime()
    likes_count = fields.Integer()
    comments_count = fields.Integer()

    @api.model
    def _fetch_feeds(self):
        accounts = self.env['social.media.account'].search([])
        for account in accounts:
            if account.platform == 'twitter':
                self._fetch_twitter_feed(account)
            elif account.platform == 'facebook':
                self._fetch_facebook_feed(account)
            elif account.platform == 'instagram':
                self._fetch_instagram_feed(account)
            elif account.platform == 'linkedin':
                self._fetch_linkedin_feed(account)

    def _fetch_twitter_feed(self, account):
        url = 'https://4951da5c-29f5-41da-8e71-7d8386bb732f.mock.pstmn.io/twitter/feed'
        response = requests.get(url)
        if response.status_code == 200:
            tweets = response.json().get('data', [])
            for tweet in tweets:
                self.create({
                    'account_id': account.id,
                    'post_id': tweet['id'],
                    'content': tweet['text'],
                    'timestamp': tweet['created_at']
                })

    def _fetch_facebook_feed(self, account):
        url = 'https://4951da5c-29f5-41da-8e71-7d8386bb732f.mock.pstmn.io/facebook/feed'
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json().get('data', [])
            for post in posts:
                self.create({
                    'account_id': account.id,
                    'post_id': post['id'],
                    'content': post.get('message', ''),
                    'timestamp': post['created_time']
                })

    def _fetch_instagram_feed(self, account):
        url = 'https://4951da5c-29f5-41da-8e71-7d8386bb732f.mock.pstmn.io/instagram/feed'
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json().get('data', [])
            for post in posts:
                self.create({
                    'account_id': account.id,
                    'post_id': post['id'],
                    'content': post.get('caption', ''),
                    'timestamp': post['timestamp']
                })

    def _fetch_linkedin_feed(self, account):
        url = f'https://api.linkedin.com/v2/shares?q=owners&owners=urn:li:person:{account.user_id}'
        headers = {'Authorization': f'Bearer {account.access_token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            shares = response.json().get('elements', [])
            for share in shares:
                self.create({
                    'account_id': account.id,
                    'post_id': share['id'],
                    'content': share.get('text', ''),
                    'timestamp': share.get('created', {}).get('time', ''),
                    'likes_count': share.get('likes', {}).get('count', 0),
                    'comments_count': share.get('comments', {}).get('count', 0),
                })
