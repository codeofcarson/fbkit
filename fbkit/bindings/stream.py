from .. import proxies

BINDINGS = {
    'addComment' : [
        ('post_id', int, {}),
        ('comment', str, {}),
        ('uid', int, {'optional': True}),
    ],
    'addLike': [
        ('uid', int, {'optional': True}),
        ('post_id', int, {'optional': True}),
    ],
    'get' : [
        ('viewer_id', int, {'optional': True}),
        ('source_ids', list, {'optional': True}),
        ('start_time', int, {'optional': True}),
        ('end_time', int, {'optional': True}),
        ('limit', int, {'optional': True}),
        ('filter_key', str, {'optional': True}),
    ],
    'getComments' : [
        ('post_id', int, {}),
    ],
    'getFilters' : [
        ('uid', int, {'optional': True}),
    ],
    'publish' : [
        ('message', str, {'optional': True}),
        ('attachment', proxies.json, {'optional': True}),
        ('action_links', proxies.json, {'optional': True}),
        ('target_id', str, {'optional': True}),
        ('uid', str, {'optional': True}),
    ],
    'remove' : [
        ('post_id', int, {}),
        ('uid', int, {'optional': True}),
    ],
    'removeComment' : [
        ('comment_id', int, {}),
        ('uid', int, {'optional': True}),
    ],
    'removeLike' : [
        ('uid', int, {'optional': True}),
        ('post_id', int, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('stream', BINDINGS)
