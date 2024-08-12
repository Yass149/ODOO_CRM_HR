from odoo import models, fields, api


class MarketingCampaign(models.Model):
    _name = 'marketing.campaign'
    _description = 'Marketing Campaign'

    name = fields.Char(string='Campaign Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    budget = fields.Float(string='Budget')
    target_audience = fields.Many2many('res.partner', string='Target Audience')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], default='draft', string='Status')
    segmentation_ids = fields.Many2many('marketing.segmentation', string='Segmentations')
    performance_tracking_ids = fields.One2many('marketing.performance.tracking', 'campaign_id', string='Performance Tracking')

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super(MarketingCampaign, self).create(vals)

    def action_start_campaign(self):
        self.write({'state': 'running'})

    def action_cancel_campaign(self):
        self.write({'state': 'cancelled'})

    def action_end_campaign(self):
        self.write({'state': 'done'})
