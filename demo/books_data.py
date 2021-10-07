from xmlrpc import client

server_url = 'http://localhost:8070'
db_name = 'second'
username = 'admin'
password = 'admin'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    search_domain = []
    books_ids = models.execute_kw(db_name, user_id, password, 'res.users',
                                  'search', [search_domain])
    print('Books ids found:', books_ids)

    books_data = models.execute_kw(db_name, user_id, password, 'res.users',
                                   'read', [books_ids, ['name']])
    print("Books data:", books_data)
else:
    print('Wrong credentials')
