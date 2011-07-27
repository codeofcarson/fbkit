from .. import proxies

BINDINGS = {
    'getAllocation': [
        ('integration_point_name', str, {}),
    ],
    'getRestrictionInfo': [],
    'setRestrictionInfo': [
        ('format', str, {'optional': True}),
        ('callback', str, {'optional': True}),
        ('restriction_str', proxies.json, {'optional': True}),
    ],
    # Some methods don't work with access_tokens, the signed option forces
    # use of the secret_key signature (avoids error 15 and, sometimes, 8) 
    'getAppProperties': [
        ('properties', list, {}),
        'signed'
    ],
    'setAppProperties': [
        ('properties', proxies.json, {}),
        'signed'
    ],
}

Proxy = proxies.build_proxy('admin', BINDINGS)
