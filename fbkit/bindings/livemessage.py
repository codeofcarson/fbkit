from .. import proxies

BINDINGS = {
    'send': [
        ('recipient', int, {}),
        ('event_name', str, {}),
        ('message', str, {}),
    ],
}

Proxy = proxies.build_proxy('livemessage', BINDINGS)
