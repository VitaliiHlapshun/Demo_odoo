from xmlrpc import client

server_url = 'http://localhost:8070'
db_name = 'second'
username = 'admin'
password = 'admin'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    create_users = [{'name': 'Umberto Gomez', 'login': 'login'},
                    {'name': 'Umberto Gomez The Second', 'login': 'login2'}
                    ]
    users_ids = models.execute_kw(db_name, user_id, password, 'res.users',
                                  'create', [create_users])
    print("Users created:", users_ids)

else:
    print('Wrong credentials')
