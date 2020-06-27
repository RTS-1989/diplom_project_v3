from urllib.parse import urlencode
import requests

OAUTH_URL = 'https://oauth.vk.com/authorize'
OAUTH_PARAMs = {
    'client_id': 7502686,
    'display': 'page',
    'scope': 'friends',
    'response_type': 'token',
    'v': 5.107
    }

print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMs))))
