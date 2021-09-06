# -*- coding: utf-8 -*-
{
    'name': "demo",

    'summary': """
        Module made for the technical task
    """,

    'description': """
        Custom module 'Demo'
    """,

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'mail'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/demo_data.xml',
        'data/data.xml',
        'views/book.xml',
        'views/book_rent.xml',
        'views/book_category.xml',
        'wizard/library_book_rent_wizard.xml',
        'wizard/library_book_return_wizard.xml',
    ],
}
