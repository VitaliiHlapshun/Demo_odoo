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
        'security/ir.model.access.csv',

        'views/book.xml',
        'views/book.xml',
        'views/book_category.xml',
    ],
}
