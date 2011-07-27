from .. import proxies

BINDINGS = {
    # setting counters for a single user
    'decrementCount': [
        ('uid', int, {}),
    ],
    'incrementCount': [
        ('uid', int, {}),
    ],
    'getCount': [
        ('uid', int, {}),
    ],
    'setCount': [
        ('uid', int, {}),
        ('count', int, {}),
    ],
    # setting counters for multiple users
    'multiDecrementCount': [
        ('uids', list, {}),
    ],
    'multiIncrementCount': [
        ('uids', list, {}),
    ],
    'multiGetCount': [
        ('uids', list, {}),
    ],
    'multiSetCount': [
        ('uids', list, {}),
    ],
    # setting news for a single user
    'addNews': [
        ('news', proxies.json, {}),
        ('image', str, {'optional': True}),
        ('uid', int, {'optional': True}),
    ],
    'getNews': [
        ('uid', int, {}),
        ('news_ids', list, {'optional': True}),
    ],
    'clearNews': [
        ('uid', int, {}),
        ('news_ids', list, {'optional': True}),
    ],
    # setting news for multiple users
    'multiAddNews': [
        ('uids', list, {}),
        ('news', proxies.json, {}),
        ('image', str, {'optional': True}),
    ],
    'multiGetNews': [
        ('uids', proxies.json, {}),
    ],
    'multiClearNews': [
        ('uids', proxies.json, {}),
    ],
    # setting application news for all users
    'addGlobalNews': [
        ('news', proxies.json, {}),
        ('image', str, {'optional': True}),
    ],
    'getGlobalNews': [
        ('news_ids', list, {'optional': True}),
    ],
    'clearGlobalNews': [
        ('news_ids', list, {'optional': True}),
    ],
    # user activity
    'getActivity': [
        ('activity_ids', list, {'optional': True}),
    ],
    'publishActivity': [
        ('activity', proxies.json, {}),
    ],
    'removeActivity': [
        ('activity_ids', list, {}),
    ],
}

Proxy = proxies.build_proxy('dashboard', BINDINGS)
