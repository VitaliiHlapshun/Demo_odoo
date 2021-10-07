from xmlrpc import client

server_url = 'http://localhost:8070'
db_name = 'second'
username = 'admin'
password = 'admin'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    book_id = models.execute_kw(db_name, user_id,
                                password,
                                'library.book', 'create',
                                [{'name': 'New Book06', 'date_release':
                                    '2019-01-26', 'state': 'borrowed',
                                  'active': True}]
                                )

    models.execute_kw(db_name, user_id, password, 'library.book',
                      'make_available', [[book_id]])

    book_data = models.execute_kw(db_name, user_id, password, 'library.book',
                                  'read', [[book_id], ['name', 'state', 'date_release']])
    #
    print('Book state after method call:', book_data)
    print('Book state after method call:', book_data[0])
    print('Book state after method call:', book_data[0]['state'])
    print("Books created:", book_id)

else:
    print('Wrong credentials')
