from odoo import models, fields, api


class MarketingPerformanceTracking(models.Model):
    _name = 'marketing.performance.tracking'
    _description = 'Marketing Performance Tracking'

    campaign_id = fields.Many2one('marketing.campaign', string='Campaign', required=True)
    total_budget = fields.Float(string='Total Budget')
    expected_revenue = fields.Float(string='Expected Revenue')
    actual_cost = fields.Float(string='Actual Cost')
    actual_revenue = fields.Float(string='Actual Revenue')
