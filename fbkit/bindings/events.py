from .. import proxies

BINDINGS = {
    'cancel': [
        ('eid', int, {}),
        ('cancel_message', str, {'optional': True}),
     ],
    'create': [
        ('event_info', proxies.json, {}),
    ],
    'edit': [
        ('eid', int, {}),
        ('event_info', proxies.json, {}),
    ],
    'get': [
        ('uid', int, {'optional': True}),
        ('eids', list, {'optional': True}),
        ('start_time', int, {'optional': True}),
        ('end_time', int, {'optional': True}),
        ('rsvp_status', str, {'optional': True}),
    ],
    'getMembers': [
        ('eid', int, {}),
    ],
    'invite': [
        ('eid', int, {}),
        ('uids', list, {}),
        ('personal_message', str, {'optional': True}),
    ],
    'rsvp': [
        ('eid', int, {}),
        ('rsvp_status', str, {}),
    ],
    'edit': [
        ('eid', int, {}),
        ('event_info', proxies.json, {}),
    ],
    'invite': [
        ('eid', int, {}),
        ('uids', list, {}),
        ('personal_message', str, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('events', BINDINGS)
