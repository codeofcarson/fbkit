from .. import proxies

BINDINGS = {
    'registerUsers': [
        ('accounts', proxies.json, {}),
    ],
    'unregisterUsers': [
        ('email_hashes', proxies.json, {}),
    ],
    'getUnconnectedFriendsCount': [],
}

Proxy = proxies.build_proxy('connect', BINDINGS)
