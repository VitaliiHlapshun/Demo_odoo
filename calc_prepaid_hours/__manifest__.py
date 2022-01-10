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
{
    'name': "Prepaid Hours Calculation",
    'summary': """Module to create manage prepaid and used hours""",
    'author': 'SmartTek',
    'license': "AGPL-3",
    'website': "https://www.smartteksas.com",
    'category': 'Extra Tools',
    'version': '14.0.6',

    'depends': ['project',
                'hr',
                'hr_timesheet',
                'account',
                'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/source.xml',
    ],
}
