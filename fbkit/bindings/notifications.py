from .. import proxies

BINDINGS = {
    'get': [],
    'send': [
        ('to_ids', list, {}),
        ('notification', str, {}),
        ('email', str, {'optional': True}),
        ('type', str, {'optional': True}),
    ],
    'sendRequest': [
        ('to_ids', list, {}),
        ('type', str, {}),
        ('content', str, {}),
        ('image', str, {}),
        ('invite', bool, {}),
    ],
    'sendEmail': [
        ('recipients', list, {}),
        ('subject', str, {}),
        ('text', str, {'optional': True}),
        ('fbml', str, {'optional': True}),
    ]
}

Proxy = proxies.build_proxy('notifications', BINDINGS)
