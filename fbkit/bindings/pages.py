from .. import proxies

BINDINGS = {
    'getInfo': [
        ('fields', list, {'default': ['page_id', 'name']}),
        ('page_ids', list, {'optional': True}),
        ('uid', int, {'optional': True}),
    ],
    'isAdmin': [
        ('page_id', int, {}),
    ],
    'isAppAdded': [
        ('page_id', int, {}),
    ],
    'isFan': [
        ('page_id', int, {}),
        ('uid', int, {}),
    ],
}

Proxy = proxies.build_proxy('pages', BINDINGS)
