from .. import proxies

BINDINGS = {
    'decodeIDs': [
        ('ids', list, {}),
    ],
}

Proxy = proxies.build_proxy('update', BINDINGS)
