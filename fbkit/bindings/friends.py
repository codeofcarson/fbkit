from .. import proxies

class FriendsProxy(proxies.Proxy):
    """Special proxy for facebook.friends."""

    def get(self, **kwargs):
        """Facebook API call. See http://developers.facebook.com/documentation.php?v=1.0&method=friends.get"""
        if not kwargs.get('flid') and self._client._friends:
            return self._client._friends
        return super(FriendsProxy, self).get(**kwargs)

BINDINGS = {
    'areFriends': [
        ('uids1', list, {}),
        ('uids2', list, {}),
    ],
    'get': [
        ('flid', int, {'optional': True}),
    ],
    'getLists': [],
    'getAppUsers': [],
    'getMutualFriends': [
        ('target_uid', int, {}),
        ('source_uid', int, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('friends', BINDINGS, FriendsProxy)
