from .. import proxies

BINDINGS = {
    'getInfo': [
        ('uids', list, {}),
        ('fields', list, {'default': ['name']}),
    ],
    'getStandardInfo': [
        ('uids', list, {}),
        ('fields', list, {'default': ['uid']}),
    ],
    'getLoggedInUser': [],
    'isAppAdded': [],
    'isAppUser': [
        ('uid', int, {}),
    ],
    'hasAppPermission': [
        ('ext_perm', str, {}),
        ('uid', int, {'optional': True}),
    ],
    'setStatus': [
        ('status', str, {}),
        ('clear', bool, {}),
        ('status_includes_verb', bool, {'optional': True}),
        ('uid', int, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('users', BINDINGS)
