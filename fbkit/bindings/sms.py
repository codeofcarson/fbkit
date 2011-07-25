from .. import proxies

BINDINGS = {
    'canSend' : [
        ('uid', int, {}),
    ],
    'send' : [
        ('uid', int, {}),
        ('message', str, {}),
        ('session_id', int, {}),
        ('req_session', bool, {}),
    ],
}

Proxy = proxies.build_proxy('sms', BINDINGS)
