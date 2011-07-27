from .. import proxies

BINDINGS = {
    'post': [
        ('url', str, {}),
        ('comment', str, {}),
        ('uid', int, {}),
        ('image', str, {'optional': True}),
        ('callback', str, {'optional': True}),
    ],
    'preview': [
        ('url', str, {}),
        ('callback', str, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('links', BINDINGS)
