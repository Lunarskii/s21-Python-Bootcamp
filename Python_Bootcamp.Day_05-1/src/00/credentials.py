from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import json

DATA = {
    'Cyberman': 'John Lumic',
    'Dalek': 'Davros',
    'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
    'Human': 'Leonardo da Vinci',
    'Ood': 'Klineman Halpen',
    'Silence': 'Tasha Lem',
    'Slitheen': 'Coca-Cola salesman',
    'Sontaran': 'General Staal',
    'Time Lord': 'Rassilon',
    'Weeping Angel': 'The Division Representative',
    'Zygon': 'Broton'
}


def application(environ, start_response):
    qs = parse_qs(environ['QUERY_STRING'])
    species = qs.get('species', None)

    if species and len(species) and species[0]:
        response_body = {'credentials': DATA.get(species[0], 'Unknown')}

        if response_body['credentials'] == 'Unknown':
            status = '404 Not Found'
        else:
            status = '200 OK'

        headers = ('Content-Type', 'application/json')
    else:
        response_body = 'Missing request parameter: species'
        status = '400 Bad Request'
        headers = ('Content-Type', 'text/plain')

    start_response(status, [headers])
    return [json.dumps(response_body).encode('utf-8')]


if __name__ == '__main__':
    httpd = make_server('localhost', 8888, application)
    httpd.serve_forever()
