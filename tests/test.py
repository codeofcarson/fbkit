import sys
from minimock import Mock
from django.utils import unittest
import urllib2
try:
    from hashlib import md5
    md5_constructor = md5
except ImportError:
    import md5
    md5_constructor = md5.new
try:
    import simplejson
except ImportError:
    from django.utils import simplejson

import fbkit

my_app_id = "249784291698385"
my_app_secret = "1ab476e5962c119b61a819e692feff77"

class FBKitTests(unittest.TestCase):
    class MockedUrlOpen(object):
        next_response = ''

        def __call__(self, *args, **kwargs):
            return self

        def read(self):
            return self.next_response

    def setUp(self):
        self.original_urlopen = urllib2.urlopen
        self.urlopen = self.MockedUrlOpen()
        urllib2.urlopen = Mock('urllib2.urlopen')
        urllib2.urlopen.mock_returns_func = self.urlopen

    def tearDown(self):
        urllib2.urlopen = self.original_urlopen

    def test_initialization(self):
        f = fbkit.Facebook(app_id=my_app_id, app_secret=my_app_secret)
        self.assertEquals(f.app_id, my_app_id)
        self.assertEquals(f.app_secret, my_app_secret)
        self.assertEquals(f.auth_token, None)
        self.assertEquals(f.app_name, None)
        self.assertEquals(f.canvas_url, None)

    def test_session_parse(self):
        response = {'stuff': 'abcd'}
        self.urlopen.next_response = simplejson.dumps(response)
        fb = fbkit.Facebook(my_app_secret, app_id=my_app_id)
        fb.auth.createToken()
        self.assertEquals(str(fb.auth_token['stuff']), "abcd")
        response = {"session_key": "key",
                    "uid": "my_uid",
                    "secret": "my_secret",
                    "expires": "my_expires"}
        self.urlopen.next_response = simplejson.dumps(response)
        res = fb.auth.getSession()
        self.assertEquals(str(res["expires"]), response["expires"])
        self.assertEquals(str(res["secret"]), response["secret"])
        self.assertEquals(str(res["session_key"]), response["session_key"])
        self.assertEquals(str(res["uid"]), response["uid"])

    def test_validate_session(self):
        session = {'sig': 'e1e94eca2c0085d0ebd7ed8216337e67',
                   'lorem': 'ipsum',
                   'dolor': 'sit amet'}
        session_json = simplejson.dumps(session)
        fb = fbkit.Facebook(my_app_secret, app_id=my_app_id)
        self.assertEqual(fb.validate_oauth_session(session_json),
                         {'lorem': 'ipsum',
                          'dolor': 'sit amet'})

    def test_login_url(self):
        response = 'abcdef'
        self.urlopen.next_response = simplejson.dumps(response)
        fb = fbkit.Facebook(my_app_secret, app_id=my_app_id)
        fb.auth.createToken()
        self.assertEquals(str(fb.auth_token), "abcdef")
        url = fb.get_login_url(next="nowhere", popup=True)
        expected = ('https://graph.facebook.com/oauth/authorize?'
                    'redirect_uri=nowhere&display=popup&client_id=%s' %
                    my_app_id)
        self.assertEquals(url, expected)

if __name__ == "__main__":

    # Build the test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FBKitTests))

    # Execute the test suite
    print("Testing Proxy class\n")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(len(result.errors) + len(result.failures))
