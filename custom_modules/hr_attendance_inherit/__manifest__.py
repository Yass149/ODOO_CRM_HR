{
    'name': "HR Attendance and Payroll Extension",
    'summary': "Extends HR attendance views with payroll and marketing functionalities",
    'description': """
        This module extends the HR attendance views and includes additional functionalities such as payroll management, employee training, email marketing, and accounting features. It provides a comprehensive solution for managing various HR activities within your organization.
    """,
    'author': "Yassine Malal",
    'website': "https://www.moroccoworldnews.com",
    'category': 'Human Resources, Accounting',
    'version': '1.0',
    'depends': ['hr_attendance', 'hr', 'base', 'crm', 'hr_recruitment'],
    'data': [
        # Data files
        'data/email_template.xml',
        'data/scheduled_action.xml',
        'data/checkin_checkout_server_actions.xml',
        'data/employee_checkin_dashboard_actions.xml',
        'data/sequence.xml',
        'data/hr_attendance_inherit_data.xml',

        # Security files
        'security/groups.xml',
        'security/custom_account_security.xml',
        'security/ir.model.access.csv',
        'security/employee_record_rules.xml',
        'security/hr_employee_security.xml',
        'security/hr_payroll_security.xml',
        'security/hr_payroll_record_rules.xml',
        'security/marketing_security.xml',
        'security/social_media_security.xml',

        # Actions
        'actions/email_marketing_actions.xml',

        # View files
        'views/attendance/hr_attendance_view_inh.xml',
        'views/attendance/hr_employee_views.xml',
        'views/employee_checkin/employee_checkin_dashboard_views.xml',
        'views/employee_checkin/employee_checkin_dashboard_menus.xml',

        # Payroll views and actions
        'views/payroll/hr_payroll_views.xml',
        'views/payroll/hr_payroll_actions.xml',
        'views/payroll/hr_payroll_menu.xml',
        'views/payroll/hr_payroll_payslip_views.xml',

        # Training views and menus
        'views/training/hr_training_views.xml',
        'views/training/hr_training_menu.xml',

        # Marketing views and actions
        'views/marketing/marketing_campaign_views.xml',
        'views/marketing/marketing_campaign_actions.xml',
        'views/marketing/marketing_segmentation_views.xml',
        'views/marketing/marketing_segmentation_actions.xml',
        'views/marketing/marketing_campaign_menu.xml',
        'views/marketing/marketing_campaign_reports.xml',

        # Email marketing views
        'views/email_marketing/email_marketing_views.xml',

        # Accounting views and actions
        'views/accounting/custom_account_views.xml',
        'views/accounting/custom_account_actions.xml',
        'views/accounting/custom_account_menus.xml',
        'views/accounting/custom_journal_entry.xml',
        'views/accounting/custom_account_reports.xml',

        'data/ir_cron.xml',
        'views/social_media_actions.xml',
        'views/social_media_views.xml',


        'views/client_partner/client_partner_views.xml',
        'views/client_partner/client_partner_actions.xml',
        'views/client_partner/client_partner_menus.xml',



    ],
    'license': 'LGPL-3',
    'demo': [],
}
