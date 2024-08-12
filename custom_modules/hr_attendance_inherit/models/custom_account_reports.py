# File: custom_modules/hr_attendance_inherit/reports/custom_account_reports.py

from odoo import models, api

class ReportBalanceSheet(models.AbstractModel):
    _name = 'report.custom_accounting.report_balance_sheet'
    _description = 'Balance Sheet Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['custom.account'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'custom.account',
            'docs': docs,
        }


class ReportIncomeStatement(models.AbstractModel):
    _name = 'report.custom_accounting.report_income_statement'
    _description = 'Income Statement Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['custom.account'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'custom.account',
            'docs': docs,
        }
