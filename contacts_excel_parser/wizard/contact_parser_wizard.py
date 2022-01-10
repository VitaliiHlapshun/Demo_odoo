# -*- coding: UTF-8 -*-
################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 SmartTek (<https://smartteksas.com/>).
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


from odoo import models, fields, exceptions
from xlrd import open_workbook

import logging, base64
from io import BytesIO

_logger = logging.getLogger(__name__)


class ProductParserWizard(models.TransientModel):
    _name = 'product.parser.wizard'

    product_file = fields.Binary(string='File')
    file_parse = fields.Boolean(string='File parsed')

    def pre_parse_file(self):
        '''Parsing of records by company type and address labels creating contacts, subcontacts and vendors
        '''
        if self.product_file:
            value = BytesIO(self.product_file).getvalue()
            file_data = base64.decodestring(value)
            book_data = open_workbook(file_contents=file_data)
            sheets = book_data.sheet_names()
            active_sheet = book_data.sheet_by_name(sheets[0])
            num_rows = active_sheet.nrows
            num_cols = active_sheet.ncols
            header = [active_sheet.cell_value(1, cell).lower()
                      for cell in range(num_cols)]
            contacts = self.env['res.partner']
            self_id = self.env['res.partner'].search([]).mapped('contact_id')
            for row_idx in range(2, num_rows):
                row_cell = [active_sheet.cell_value(row_idx, col_idx)
                            for col_idx in range(num_cols)]
                vals = dict(zip(header, row_cell))
                if vals['id'] not in self_id:
                    try:
                        property_account_position_id = int(vals.get('fiscal position'))
                        if not property_account_position_id:
                            property_account_position_id = False
                    except:
                        property_account_position_id = False
                    try:
                        property_product_pricelist = int(vals.get('pricelist'))
                        if not property_product_pricelist:
                            property_product_pricelist = False
                    except:
                        property_product_pricelist = False
                    try:
                        property_account_receivable_id = int(vals.get('account receivable'))
                        if not property_account_receivable_id:
                            property_account_receivable_id = False
                    except:
                        property_account_receivable_id = False
                    try:
                        property_account_payable_id = int(vals.get('account payable'))
                        if not property_account_payable_id:
                            property_account_payable_id = False
                    except:
                        property_account_payable_id = False
                    try:
                        language = (vals.get('language'))
                        lang = self.env['res.lang'].search([('code', '=', language)])
                        if not lang or not lang.active:
                            language = None
                    except:
                        language = None
                    """Defining business partner
                    """
                    if vals.get('company type') in ['business', 'supplier']:
                        business_contact = contacts.create(
                            {'contact_id': vals['id'],
                             'company_type': 'company',
                             'property_account_position_id': property_account_position_id,
                             'property_product_pricelist': property_product_pricelist,
                             'property_account_receivable_id': property_account_receivable_id,
                             'property_account_payable_id': property_account_payable_id,
                             'lang': language,
                             'name': vals['name'],
                             'email': vals['email'],
                             'phone': vals['phone number'],
                             'vat': vals['tax number'],
                             'supplier_rank': 1 if vals.get(
                                 'company type') == 'supplier' else 0,
                             })
                        """Defining main contact of business partner
                        """
                        if vals.get('contact name') and not vals.get(
                                'company type') == 'consumer':
                            contacts.create(
                                {'contact_id': vals['id'],
                                 'company_type': 'person',
                                 'name': vals['contact name'],
                                 'property_account_position_id': property_account_position_id,
                                 'lang': language,
                                 'type': 'contact',
                                 'phone': vals['contact phone number'],
                                 'email': vals['contact email'],
                                 'function': vals['contact position'],
                                 'comment': vals['contact notes'],
                                 'mobile': vals['contact mobile'],
                                 'parent_id': business_contact.id,
                                 'supplier_rank': 1 if vals.get(
                                     'company type') == 'supplier' else 0})
                        """Defining subcontacts
                        """
                        for i in range(1, 11):
                            if vals.get(f'address {i} label'):
                                """Defining main contact of business partner 1"""
                                values = self.get_subcontact_values(
                                    vals, i, business_contact)
                                values.update({'supplier_rank': 1 if vals.get(
                                    'company type') == 'supplier' else 0, })
                                contacts.create(values)
                        """Defining consumer partner
                        """
                    elif vals.get('company type') == 'consumer':
                        customer_contact = contacts.create({
                            'contact_id': vals['id'],
                            'name': vals['contact name'],
                            'property_account_position_id': property_account_position_id,
                            'property_product_pricelist': property_product_pricelist,
                            'property_account_receivable_id': property_account_receivable_id,
                            'property_account_payable_id': property_account_payable_id,
                            'lang': language,
                            'company_type': 'person',
                            'phone': vals['contact phone number'],
                            'email': vals['contact email'],
                            'function': vals['contact position'],
                            'comment': vals['contact notes'],
                            'mobile': vals['contact mobile'],
                        })
                        """Defining subcontacts
                                       """
                        for i in range(1, 11):
                            if vals.get(f'address {i} label') and vals.get('company type') == 'consumer':
                                """Defining main contact of business partner 1"""
                                values = self.get_subcontact_values(
                                    vals, i, customer_contact)
                                contacts.create(values)

    def get_subcontact_values(self, vals, i, contact):
        try:
            property_account_position_id = int(vals.get('fiscal position'))
            if not property_account_position_id:
                property_account_position_id = False
        except:
            property_account_position_id = False
        try:
            language = (vals.get('language'))
            lang = self.env['res.lang'].search([('code', '=', language)])
            if not lang or not lang.active:
                language = None
        except:
            language = None
        try:
            state_id = int(vals.get(f'address {i} state'))
            if not state_id:
                state_id = False
        except:
            state_id = False
        try:
            country_id = int(vals.get(f'address {i} country'))
            if not country_id:
                country_id = False
        except:
            country_id = False
        try:
            zip = int(vals.get(f'address {i} zip code'))
            if not zip:
                zip = False
        except:
            zip = False
        return {'contact_id': vals['id'],
                'company_type': 'person',
                'type': 'invoice' if vals[f'address {i} label'] == 'Billing' else 'delivery',
                'name': vals[f'address {i} company name'],
                'property_account_position_id': property_account_position_id,
                'lang': language,
                'street': vals[f'address {i} line 1'],
                'street2': str(vals[f'address {i} line 2']) + ', ' + str(
                    vals[f'address {i} suburb']),
                'city': vals[f'address {i} city'],
                'state_id': state_id,
                'zip': zip,
                'country_id': country_id,
                'phone': vals[f'address {i} phone number'],
                'email': vals[f'address {i} email'],
                'parent_id': contact.id,
                }
