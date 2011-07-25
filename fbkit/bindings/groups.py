from .. import proxies

BINDINGS = {
    'get': [
        ('uid', int, {'optional': True}),
        ('gids', list, {'optional': True}),
    ],
    'getMembers': [
        ('gid', int, {}),
    ],
}

Proxy = proxies.build_proxy('groups', BINDINGS)
