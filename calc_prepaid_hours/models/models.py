################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 SmartTek (<https://smartteksas.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    project_prepaid_hour_ids = fields.One2many('project.prepaid.hour',
                                               'project_id',
                                               string='Prepaid Hours')

    prepaid_hours = fields.Float(string='Prepaid Hours',
                                 compute='_get_prepaid_hours',
                                 default=0.00,
                                 store=True)

    using_prepaid_hours = fields.Float(string='Using Prepaid Hours',
                                       compute='_get_prepaid_hours',
                                       default=0.00,
                                       store=True)

    @api.depends('project_prepaid_hour_ids', 'task_ids.timesheet_ids')
    def _get_prepaid_hours(self):
        for project in self:
            prepaid_hours = 0.0
            for project_prepaid_hour_id in project.project_prepaid_hour_ids:
                prepaid_hours += project_prepaid_hour_id.hours
            project.prepaid_hours = prepaid_hours
            using_prepaid_hours = 0.0

            if not project.project_prepaid_hour_ids:
                continue

            prepaid_date = project.project_prepaid_hour_ids[0].date
            if project.project_prepaid_hour_ids:
                timesheet_ids = self.env['account.analytic.line'].search(
                    [('project_id', '=', project.id)])
                for timesheet_id in timesheet_ids:
                    if prepaid_date and timesheet_id.date and timesheet_id.date >= prepaid_date:
                        using_prepaid_hours += timesheet_id.unit_amount
            project.using_prepaid_hours = using_prepaid_hours


class ProjectPrepaidHour(models.Model):
    _name = "project.prepaid.hour"
    _order = "date"

    project_id = fields.Many2one('project.project', string="Project")
    date = fields.Date(string='Date', required=True)
    hours = fields.Integer(string='Prepaid Hours', required=True)
