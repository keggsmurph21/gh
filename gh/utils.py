import urllib.request as urllib

import getpass
import json

from base64 import b64encode
from collections import defaultdict

STATE = defaultdict(None)

def register_state(**kwargs):
    for key, value in kwargs.items():
        STATE[key] = value

class GHError(ValueError):
    def __init__(self, op, err):
        msg = f'{STATE.get("username")}/{STATE.get("repo")}@{STATE.get("branch")} ' \
            + f'{op} returned {err.code}: {err.reason}'
        super(GHError, self).__init__(msg)

class GHRequest(urllib.Request):

    DOMAIN = None

    def __init__(self, url, **headers):

        url = f'https://{self.DOMAIN}{url}'
        data = None
        method = 'GET'

        if 'data' in headers.keys():
            method = 'POST'
            headers['Content-Type'] = 'application/json'
            data = json.dumps(headers.pop('data')).encode()
        if STATE.get('token') is None:
            if STATE.get('password') is None:
                STATE['password'] = getpass.getpass(f'{STATE.get("username")} password: ')
            credentials = f'{STATE.get("username")}:{STATE.get("password")}'
            b64creds = b64encode(credentials.encode()).decode()
            basic_auth = f'Basic {b64creds}'
            headers['Authorization'] = basic_auth
        else:
            token_auth = f'token {STATE.get("token")}'
            headers['Authorization'] = token_auth

        print(url, data, method, headers)
        super(GHRequest, self).__init__(
                url,
                data=data,
                method=method,
                headers=headers
        )

class APIRequest(GHRequest):
    DOMAIN = 'api.github.com'

class RawRequest(GHRequest):
    DOMAIN = 'raw.githubusercontent.com'

def call(url, **kwargs):
    try:
        req = APIRequest(url, **kwargs)
        res = urllib.urlopen(req)
        return None, json.load(res)
    except urllib.HTTPError as e:
        return e, None

def repo_exists():
    err, _ = call(f'/repos/{STATE.get("username")}/{STATE.get("repo")}')
    if err is None:
        return True
    elif err.code == 404:
        return False
    else:
        raise GHError('repo-exists', err)

