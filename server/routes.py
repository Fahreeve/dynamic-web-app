from server.views import *

routes = [
    ('GET', '/login', login, 'login_page'),
    ('POST', '/login', login, 'login'),
    ('GET', '/logout', logout, 'logout'),
    ('GET', '/registration', registration, 'registration_page'),
    ('POST', '/registration', registration, 'registration'),
    ('GET', '/file/{name}', get_files, 'file'),
    ('GET', '/bigfile/{name}', get_big_files, 'bigfile'),
    ('GET', '/db', db_request, 'db_page'),
    ('POST', '/db', db_request, 'db'),
    ('GET', '/calc', calculate, 'calc'),
    ('GET', '/ping', ping, 'ping')
]
