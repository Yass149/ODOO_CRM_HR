# -*- coding: utf-8 -*-
# from odoo import http


# class HrAttendanceInherit(http.Controller):
#     @http.route('/hr_attendance_inherit/hr_attendance_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_attendance_inherit/hr_attendance_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_attendance_inherit.listing', {
#             'root': '/hr_attendance_inherit/hr_attendance_inherit',
#             'objects': http.request.env['hr_attendance_inherit.hr_attendance_inherit'].search([]),
#         })

#     @http.route('/hr_attendance_inherit/hr_attendance_inherit/objects/<model("hr_attendance_inherit.hr_attendance_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_attendance_inherit.object', {
#             'object': obj
#         })

