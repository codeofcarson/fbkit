from .. import proxies

BINDINGS = {
    'get': [
        ('uid', int, {'optional': True}),
        ('limit', int, {'optional': True}),
    ],
    'set': [
        ('status', str, {'optional': True}),
        ('uid', int, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('status', BINDINGS)
