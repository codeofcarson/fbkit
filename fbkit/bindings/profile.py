from .. import proxies

BINDINGS = {
    'setFBML': [
        ('markup', str, {'optional': True}),
        ('uid', int, {'optional': True}),
        ('profile', str, {'optional': True}),
        ('profile_action', str, {'optional': True}),
        ('mobile_fbml', str, {'optional': True}),
        ('profile_main', str, {'optional': True}),
    ],
    'getFBML': [
        ('uid', int, {'optional': True}),
        ('type', int, {'optional': True}),
    ],
    'setInfo': [
        ('title', str, {}),
        ('type', int, {}),
        ('info_fields', proxies.json, {}),
        ('uid', int, {}),
    ],
    'getInfo': [
        ('uid', int, {}),
    ],
    'setInfoOptions': [
        ('field', str, {}),
        ('options', proxies.json, {}),
    ],
    'getInfoOptions': [
        ('field', str, {}),
    ],
}

Proxy = proxies.build_proxy('profile', BINDINGS)
