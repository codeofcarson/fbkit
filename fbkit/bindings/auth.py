from .. import proxies

class AuthProxy(proxies.Proxy):
    """Special proxy for facebook.auth."""

    def getSession(self):
        """Facebook API call. See http://developers.facebook.com/documentation.php?v=1.0&method=auth.getSession"""
        args = {}
        try:
            args['auth_token'] = self._client.auth_token
        except AttributeError:
            raise RuntimeError('Client does not have auth_token set.')
        try:
            args['generate_session_secret'] = self._client.generate_session_secret
        except AttributeError:
            pass
        result = self._client('%s.getSession' % self._name, args)
        self._client.session_key = result['session_key']
        self._client.uid = result['uid']
        self._client.secret = result.get('secret')
        self._client.session_key_expires = result['expires']
        return result

    def createToken(self):
        """Facebook API call. See http://developers.facebook.com/documentation.php?v=1.0&method=auth.createToken"""
        token = self._client('%s.createToken' % self._name)
        self._client.auth_token = token
        return token

BINDINGS = {
    'revokeAuthorization': [
        ('uid', int, {'optional': True}),
    ],
    'revokeExtendedPermission': [
        ('perm', str, {}),
        ('uid', int, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('auth', BINDINGS, AuthProxy)
