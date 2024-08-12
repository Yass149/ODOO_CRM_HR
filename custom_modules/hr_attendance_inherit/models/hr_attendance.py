# models/hr_attendance.py

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from geopy.distance import geodesic

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    in_latitude = fields.Float(string='Check-in Latitude')
    in_longitude = fields.Float(string='Check-in Longitude')
    out_latitude = fields.Float(string='Check-out Latitude')
    out_longitude = fields.Float(string='Check-out Longitude')

    @api.model
    def create(self, vals):
        employee = self.env['hr.employee'].browse(vals['employee_id'])
        if not employee.can_work_remotely:
            if 'in_latitude' in vals and 'in_longitude' in vals:
                latitude = vals['in_latitude']
                longitude = vals['in_longitude']
                if not self._is_within_allowed_area(latitude, longitude):
                    raise ValidationError(_('You can only check in from an allowed location.'))

            if 'out_latitude' in vals and 'out_longitude' in vals:
                latitude = vals['out_latitude']
                longitude = vals['out_longitude']
                if not self._is_within_allowed_area(latitude, longitude):
                    raise ValidationError(_('You can only check out from an allowed location.'))

        return super(HrAttendance, self).create(vals)

    def _is_within_allowed_area(self, latitude, longitude):
        # Define the office location
        office_latitude = 34.0194
        office_longitude = -6.8361
        office_tolerance = 0.01  # Define a tolerance range for the office location

        def is_within_tolerance(lat, lon, allowed_lat, allowed_lon, tolerance):
            return (
                allowed_lat - tolerance <= lat <= allowed_lat + tolerance and
                allowed_lon - tolerance <= lon <= allowed_lon + tolerance
            )

        # Check if within office location
        if is_within_tolerance(latitude, longitude, office_latitude, office_longitude, office_tolerance):
            return True

        # Check if within any approved remote work location
        requests = self.env['remote.work.request'].search([('employee_id.user_id', '=', self.env.user.id), ('state', '=', 'approved')])
        for request in requests:
            if self._is_within_radius(latitude, longitude, request.latitude, request.longitude, request.radius):
                return True

        return False

    def _is_within_radius(self, lat1, lon1, lat2, lon2, radius):
        location_point = (lat2, lon2)
        user_point = (lat1, lon1)
        distance = geodesic(location_point, user_point).meters
        return distance <= radius
