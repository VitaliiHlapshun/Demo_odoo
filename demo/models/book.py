# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char('Title', required=True)
    active = fields.Boolean()
    date_release = fields.Date('Release Date')
    isbn = fields.Char('ISBN')
    pages = fields.Integer('Number of Pages')
    short_name = fields.Char('Short Title', translate=True, index=True)
    cost_price = fields.Float('Book Cost')
    author_ids = fields.Many2many('res.partner', string='Authors')
    old_edition = fields.Many2one('library.book', string='Old Edition')
    category_id = fields.Many2one('library.book.category')
    state = fields.Selection(
        [('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
        'State', default="available")
    publisher_id = fields.Many2one('res.partner', string='Publisher',
                                   # optional:
                                   ondelete='set null',
                                   context={},
                                   domain=[],
                                   )

    @api.model
    def _update_book_price(self):
        all_books = self.search([])
        for book in all_books:
            book.cost_price += 10

    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def grouped_data(self):
        data = self.get_average_cost()
        logger.info("Groupped Data %s" % data)

    def get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price', "!=", False)],  # Domain
            ['category_id', 'cost_price:avg'],  # Fields to access
            ['date_release:month']  # group_by
        )
        return grouped_result

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|', '|',
                     ('name', operator, name),
                     ('isbn', operator, name),
                     ('author_ids.name', operator, name)
                     ]
        return super(LibraryBook, self)._name_search(
            name=name, args=args, operator=operator,
            limit=limit, name_get_uid=name_get_uid)

    def name_get(self):
        result = []
        for book in self:
            authors = book.author_ids.mapped('name')
            name = f'{book.date_release}, {book.name}'
            result.append((book.id, name))
        return result

    # Filter recordset
    def filter_books(self):
        for book in self:
            all_books = self.search([])
            qty_authors = len(book.author_ids)
            filtered_books = book.env['library.book'].search([(qty_authors, '>', 1)]).mapped('name')
            self.name_get()
            print(filtered_books)
            logger.info('Filtered Books: %s', filtered_books)

    def books_with_multiple_authors(self, all_books):
        def predicate(book):
            if len(book.author_ids) >= 1:
                return True

        return all_books.filtered(predicate)

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue

    def ref_check(self):
        '''returns recordset of view-ids'''
        ref = self.env.ref("demo.library_book_view_tree").id
        print(ref)

    def make_available(self):
        self.ensure_one()
        self.state = 'available'

    def make_borrowed(self):
        self.ensure_one()
        self.state = 'borrowed'

    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'
        if not self.env.context.get('avoid_deactivate'):
            self.active = False

    def book_rent(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError(_('Book is not available for renting'))
        rent_as_superuser = self.env['library.book.rent'].sudo()
        print(rent_as_superuser)
        rent_as_superuser.create({
            'book_id': self.id,
            'borrower_id': self.env.user.partner_id.id,
        })

    def loose_all_book(self):
        all_books = self.env['library.book']
        books = all_books.search([])
        print(f'All books -> {books}')
        print(f'All books -> {all_books}')

    def change_release(self):
        # self.ensure_one()
        self.write({
            'date_release': fields.Datetime.now(),
        })

    def log_all_library_members(self):
        library_member_model = self.env['library.member']  # This is an empty recordset of model library.member
        all_members = library_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (1, 49, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be craeted in library.book.category model
        record = self.env['library.book.category'].create(parent_category_val)
        return True
        # explaining of update() method

    def change_release_date(self):
        today = fields.Datetime.now()
        # self.ensure_one()
        self.update({
            'date_release': today,
        })

    def average_book_occupation(self):
        self.flush()
        sql_query = """
            SELECT
                lb.name,
                avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
            FROM
                library_book_rent AS lbr
            JOIN
                library_book as lb ON lb.id = lbr.book_id
            WHERE lbr.state = 'returned'
            GROUP BY lb.name;"""
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        logger.info("Average book occupation: %s", result)


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Library member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
