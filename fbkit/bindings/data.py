from .. import proxies

BINDINGS = {
    'getCookies': [
        ('uid', int, {}),
        ('string', str, {'optional': True}),
    ],
    'setCookie': [
        ('uid', int, {}),
        ('name', str, {}),
        ('value', str, {}),
        ('expires', int, {'optional': True}),
        ('path', str, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('data', BINDINGS)
