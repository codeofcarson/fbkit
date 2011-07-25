from .. import proxies

BINDINGS = {
    'getPublicInfo': [
        ('application_id', int, {'optional': True}),
        ('application_api_key', str, {'optional': True}),
        ('application_canvas_name', str, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('application', BINDINGS)
