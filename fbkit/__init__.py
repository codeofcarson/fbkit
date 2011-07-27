#! /usr/bin/env python
#
# pyfacebook - Python bindings for the Facebook API
#
# Copyright (c) 2008, Samuel Cormier-Iijima
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Python bindings for the Facebook API (pyfacebook - http://code.google.com/p/pyfacebook)

PyFacebook is a client library that wraps the Facebook API.

For more information, see

Home Page: http://code.google.com/p/pyfacebook
Developer Wiki: http://wiki.developers.facebook.com/index.php/Python
Facebook IRC Channel: #facebook on irc.freenode.net

PyFacebook can use simplejson if it is installed, which
is much faster than XML and also uses less bandwith. Go to
http://undefined.org/python/#simplejson to download it, or do
apt-get install python-simplejson on a Debian-like system.
"""
import base64
import hmac
import time
import urllib
import urllib2
import urlparse
try:
    import hashlib
except ImportError:
    import md5 as hashlib

from django.conf import settings

from . import bindings, graph, urlread

VERSION = (2011, 7, 0, 'pre', 0)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version

# try to use simplejson first, otherwise fallback to XML
RESPONSE_FORMAT = 'JSON'
try:
    import json as simplejson
    simplejson.loads
except (ImportError, AttributeError):
    try:
        import simplejson
        simplejson.loads
    except (ImportError, AttributeError):
        try:
            from django.utils import simplejson
            simplejson.loads
        except (ImportError, AttributeError):
            try:
                import jsonlib as simplejson
                simplejson.loads
            except (ImportError, AttributeError):
                from xml.dom import minidom
                RESPONSE_FORMAT = 'XML'

__all__ = ['Facebook', 'create_hmac']

FACEBOOK_URL = 'http://api.facebook.com/restserver.php'
FACEBOOK_VIDEO_URL = 'http://api-video.facebook.com/restserver.php'
FACEBOOK_SECURE_URL = 'https://api.facebook.com/restserver.php'


def create_hmac(tbhashed):
    return hmac.new(settings.SECRET_KEY, tbhashed, hashlib.sha1).hexdigest()


class FacebookError(Exception):
    """
    Exception class for errors received from Facebook.
    """

    def __init__(self, code, msg, args=None):
        self.code = code
        self.msg = msg
        self.extra_args = args
        Exception.__init__(self, code, msg, args)

    def __str__(self):
        return 'Error %s: %s' % (self.code, self.msg)


class Facebook(object):
    """
    Provides access to the Facebook API.

    Instance Variables:

    added
        True if the user has added this application.

    app_id
        Your application id, as set in the constructor or fetched from
        fb_sig_app_id request parameter. This is also the app's key.

    app_name
        Your application's name, i.e. the APP_NAME in http://apps.facebook.com/APP_NAME/ if
        this is for a web application. Optional, but useful for automatic redirects
        to canvas pages.

    auth_token
        The auth token that Facebook gives you, either with facebook.auth.createToken,
        or through a GET parameter.

    callback_path
        The path of the callback set in the Facebook app settings. If your callback is set
        to http://www.example.com/facebook/callback/, this should be '/facebook/callback/'.
        Optional, but useful for automatic redirects back to the same page after login.

    desktop
        True if this is a desktop app, False otherwise. Used for determining how to
        authenticate.

    ext_perms
        Any extended permissions that the user has granted to your application.
        This parameter is set only if the user has granted any.

    facebook_url
        The url to use for Facebook requests.

    facebook_secure_url
        The url to use for secure Facebook requests.

    locale
        The user's locale. Default: 'en_US'

    oauth2_token:
        The current OAuth 2.0 token.
    
    oauth2_token_expires:
        The UNIX time when the OAuth 2.0 token expires (seconds).

    page_id
        Set to the page_id of the current page (if any)

    profile_update_time
        The time when this user's profile was last updated. This is a UNIX timestamp. Default: None if unknown.

    secret
        Secret that is used after getSession for desktop apps.

    app_secret
        Your application's secret key, as set in the constructor.

    session_key
        The current session key. Set automatically by auth.getSession, but can be set
        manually for doing infinite sessions.

    session_key_expires
        The UNIX time of when this session key expires, or 0 if it never expires.

    uid
        After a session is created, you can get the user's UID with this variable. Set
        automatically by auth.getSession.

    ----------------------------------------------------------------------

    """

    def __init__(self, app_secret, auth_token=None, app_name=None,
                 callback_path=None, proxy=None, facebook_url=None,
                 facebook_secure_url=None, generate_session_secret=0,
                 app_id=None):
        """
        Initializes a new Facebook object which provides wrappers for the Facebook API.

        If this is a desktop application, the next couple of steps you might want to take are:

        facebook.auth.createToken() # create an auth token
        wait_login()                # somehow wait for the user to log in
        facebook.auth.getSession()  # get a session key

        For web apps, if you are passed an auth_token from Facebook, pass that in as a named parameter.
        Then call:

        facebook.auth.getSession()

        """
        self.app_secret = app_secret
        self.app_id = app_id
        self.oauth2_token = None
        self.oauth2_token_expires = None
        self.session_key = None
        self.session_key_expires = None
        self.auth_token = auth_token
        self.secret = None
        self.generate_session_secret = generate_session_secret
        self.uid = None
        self.page_id = None
        self.added = False
        self.app_name = app_name
        self.callback_path = callback_path
        self._friends = None
        self.locale = 'en_US'
        self.profile_update_time = None
        self.ext_perms = []
        self.proxy = proxy
        if facebook_url is None:
            self.facebook_url = FACEBOOK_URL
        else:
            self.facebook_url = facebook_url
        if facebook_secure_url is None:
            self.facebook_secure_url = FACEBOOK_SECURE_URL
        else:
            self.facebook_secure_url = facebook_secure_url

        self.graph = graph.Graph(self)

        for namespace, klass in bindings.PROXIES.iteritems():
            setattr(self, namespace, klass(self))

    def _hash_args(self, args, secret=None):
        """Hashes arguments by joining key=value pairs, appending a secret, and then taking the MD5 hex digest."""
        # @author: houyr
        # fix for UnicodeEncodeError
        hasher = hashlib.md5(''.join(['%s=%s' % (isinstance(x, unicode) and x.encode("utf-8") or x, isinstance(args[x], unicode) and args[x].encode("utf-8") or args[x]) for x in sorted(args.keys())]))
        if secret:
            hasher.update(secret)
        elif self.secret:
            hasher.update(self.secret)
        else:
            hasher.update(self.app_secret)
        return hasher.hexdigest()


    def _parse_response_item(self, node):
        """Parses an XML response node from Facebook."""
        if node.nodeType == node.DOCUMENT_NODE and \
            node.childNodes[0].hasAttributes() and \
            node.childNodes[0].hasAttribute('list') and \
            node.childNodes[0].getAttribute('list') == "true":
            return {node.childNodes[0].nodeName: self._parse_response_list(node.childNodes[0])}
        elif node.nodeType == node.ELEMENT_NODE and \
            node.hasAttributes() and \
            node.hasAttribute('list') and \
            node.getAttribute('list')=="true":
            return self._parse_response_list(node)
        elif len(filter(lambda x: x.nodeType == x.ELEMENT_NODE, node.childNodes)) > 0:
            return self._parse_response_dict(node)
        else:
            return ''.join(node.data for node in node.childNodes if node.nodeType == node.TEXT_NODE)

    def _parse_response_dict(self, node):
        """Parses an XML dictionary response node from Facebook."""
        result = {}
        for item in filter(lambda x: x.nodeType == x.ELEMENT_NODE, node.childNodes):
            result[item.nodeName] = self._parse_response_item(item)
        if node.nodeType == node.ELEMENT_NODE and node.hasAttributes():
            if node.hasAttribute('id'):
                result['id'] = node.getAttribute('id')
        return result

    def _parse_response_list(self, node):
        """Parses an XML list response node from Facebook."""
        result = []
        for item in filter(lambda x: x.nodeType == x.ELEMENT_NODE, node.childNodes):
            result.append(self._parse_response_item(item))
        return result

    def _check_error(self, response):
        """Checks if the given Facebook response is an error, and then raises the appropriate exception."""
        if type(response) is dict and response.has_key('error_code'):
            raise FacebookError(response['error_code'], response['error_msg'], response['request_args'])

    def _build_post_args(self, method, args=None, signed=False):
        """Adds to args parameters that are necessary for every call to the API."""
        if args is None:
            args = {}

        for arg in args.items():
            if type(arg[1]) == list:
                args[arg[0]] = ','.join(str(a) for a in arg[1])
            elif type(arg[1]) == unicode:
                args[arg[0]] = arg[1].encode("UTF-8")
            elif type(arg[1]) == bool:
                args[arg[0]] = str(arg[1]).lower()

        args['method'] = method
        args['format'] = RESPONSE_FORMAT
        if not signed and self.oauth2_token:
            args['access_token'] = self.oauth2_token

        return args

    def _parse_response(self, response, method, format=None):
        """Parses the response according to the given (optional) format, which should be either 'JSON' or 'XML'."""
        if not format:
            format = RESPONSE_FORMAT

        if format == 'JSON':
            result = simplejson.loads(response)

            self._check_error(result)
        elif format == 'XML':
            dom = minidom.parseString(response)
            result = self._parse_response_item(dom)
            dom.unlink()

            if 'error_response' in result:
                self._check_error(result['error_response'])

            result = result[method[9:].replace('.', '_') + '_response']
        else:
            raise RuntimeError('Invalid format specified.')

        return result

    def unicode_urlencode(self, params):
        """
        @author: houyr
        A unicode aware version of urllib.urlencode.
        """
        if isinstance(params, dict):
            params = params.items()
        return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v)
                          for k, v in params])

    def __call__(self, method=None, args=None, signed=False):
        """Make a call to Facebook's REST server."""
        # for Django templates, if this object is called without any arguments
        # return the object itself
        if method is None:
            return self

        # __init__ hard-codes into en_US
        if args is not None and not args.has_key('locale'):
            args['locale'] = self.locale

        # @author: houyr
        # fix for bug of UnicodeEncodeError
        post_data = self.unicode_urlencode(self._build_post_args(method, args, signed))

        if self.proxy:
            proxy_handler = urllib2.ProxyHandler(self.proxy)
            opener = urllib2.build_opener(proxy_handler)
            response = opener.open(self.facebook_secure_url, post_data).read()
        else:
            response = urlread.urlread(self.facebook_secure_url, post_data)

        return self._parse_response(response, method)

    def oauth2_access_token(self, code, next, required_permissions=None):
        """
        We've called authorize, and received a code, now we need to convert
        this to an access_token
        
        """
        args = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'redirect_uri': next,
            'code': code
        }

        if required_permissions:
            args['scope'] = ",".join(required_permissions)

        # TODO see if immediate param works as per OAuth 2.0 spec?
        url = self.get_graph_url('oauth/access_token', **args)
        
        if self.proxy:
            proxy_handler = urllib2.ProxyHandler(self.proxy)
            opener = urllib2.build_opener(proxy_handler)
            response = opener.open(url).read()
        else:
            response = urlread.urlread(url)

        result = urlparse.parse_qs(response)
        self.oauth2_token = result['access_token'][0]
        if 'expires' in result:
            self.oauth2_token_expires = time.time() + int(result['expires'][0])

    def get_app_url(self, path=''):
        """
        Returns the URL for this app's canvas page, according to app_name.

        """
        return 'http://apps.facebook.com/%s/%s' % (self.app_name, path)

    def get_graph_url(self, path='', **args):
        """
        Returns the URL for the graph API with the supplied path and parameters

        """
        return 'https://graph.facebook.com/%s?%s' % (path, urllib.urlencode(args))

    def get_login_url(self, next=None, popup=False, required_permissions=None):
        """
        Returns the URL that the user should be redirected to in order to login.

        next -- the URL that Facebook should redirect to after login
        required_permissions -- permission required by the application

        """
        args = {
            'client_id': self.app_id,
            'redirect_uri': next
        }

        if required_permissions:
            args['scope'] = required_permissions
        if popup:
            args['display'] = 'popup'

        return self.get_graph_url('oauth/authorize', **args)

    def validate_oauth_session(self, session_json):
        session = simplejson.loads(session_json)
        sig = session.pop('sig')
        hash = self._hash_args(session)
        if hash == sig:
            return session
        return None

    def validate_oauth_signed_request(self, signed_request):
        sig, payload = map(str, signed_request.split('.', 1))
        def pad(string):
            if len(string) % 4:
                return string + '=' * (4 - len(string) % 4)
            return string
        try:
            sig = base64.urlsafe_b64decode(pad(sig))
            data = base64.urlsafe_b64decode(pad(payload))
            data = simplejson.loads(data)
        except:
            return None
        if data['algorithm'] != 'HMAC-SHA256':
            return None
        digest = hmac.new(settings.FACEBOOK_APP_SECRET, payload, hashlib.sha256).digest()
        if str(digest) != sig:
            return None
        return {
            'access_token': data.get('oauth_token', None),
            'expires': data.get('expires', None) or None,
            'uid': data.get('user_id', None),
            'session_key': None,
        }

if __name__ == '__main__':
    # sample desktop application

    app_id = ''
    app_secret = ''

    facebook = Facebook(app_id, app_secret)

    facebook.auth.createToken()

    # Login to the window, then press enter
    print 'After logging in, press enter...'
    raw_input()

    facebook.auth.getSession()
    print 'Session Key:   ', facebook.session_key
    print 'Your UID:      ', facebook.uid

    info = facebook.users.getInfo([facebook.uid], ['name', 'birthday', 'affiliations', 'sex'])[0]

    print 'Your Name:     ', info['name']
    print 'Your Birthday: ', info['birthday']
    print 'Your Gender:   ', info['sex']

    friends = facebook.friends.get()
    friends = facebook.users.getInfo(friends[0:5], ['name', 'birthday', 'relationship_status'])

    for friend in friends:
        print friend['name'], 'has a birthday on', friend['birthday'], 'and is', friend['relationship_status']

    arefriends = facebook.friends.areFriends([friends[0]['uid']], [friends[1]['uid']])

    photos = facebook.photos.getAlbums(facebook.uid)

