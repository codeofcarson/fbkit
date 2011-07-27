from .. import proxies

BINDINGS = {
    'query': [
        ('query', str, {}),
    ],
    'multiquery': [
        ('queries', proxies.json, {}),
    ],
}

Proxy = proxies.build_proxy('fql', BINDINGS)
