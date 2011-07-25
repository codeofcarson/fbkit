from .. import proxies

BINDINGS = {
    'add': [
        # text should be after xid/object_id, but is required
        ('text', str, {}),
        # One of xid and object_is is required. Can this be expressed?
        ('xid', str, {'optional': True}),
        ('object_id', str, {'optional': True}),
        ('uid', int, {'optional': True}),
        ('title', str, {'optional': True}),
        ('url', str, {'optional': True}),
        ('publish_to_stream', bool, {'default': False}),
    ],
    'remove': [
        # One of xid and object_is is required. Can this be expressed?
        ('xid', str, {'optional': True}),
        ('object_id', str, {'optional': True}),
        # comment_id should be required
        ('comment_id', str, {'optional': True}),
    ],
    'get': [
        # One of xid and object_is is required. Can this be expressed?
        ('xid', str, {'optional': True}),
        ('object_id', str, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('comments', BINDINGS)
