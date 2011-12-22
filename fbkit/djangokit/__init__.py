import datetime
import decorator
import logging
import time
import urllib
import urlparse

from .. import Facebook, FacebookError

from django.http import HttpResponseRedirect
from django.conf import settings

__all__ = ['Facebook', 'FacebookMiddleware', 'require_oauth']

class Facebook(Facebook):
    def oauth2_load_session(self, data):
        if data and 'access_token' in data:
            self.oauth2_token = data['access_token']
            self.oauth2_token_expires = data['expires']
            self.session_key = data['session_key']
        if data and 'uid' in data:
            self.uid = data['uid']

    def oauth2_save_session(self):
        return {
            'access_token': self.oauth2_token,
            'expires': self.oauth2_token_expires,
            'session_key': self.session_key,
            'uid': self.uid,
        }

    def oauth2_check_session(self, request):
        """
        Check to see if we have an access_token in our session
        """
        valid_token = False

        # See if we've got this user's access_token in our session
        if self.oauth2_token:
            if self.oauth2_token_expires:
                if self.oauth2_token_expires > time.time():
                    # Got a token, and it's valid
                    valid_token = True
                else:
                    del request.session['facebook']
            else:
                # does not expire
                valid_token = True

        return valid_token

    def oauth2_clear_state(self, request):
        if 'oauth2_extended_permissions' in request.session:
            del request.session['oauth2_extended_permissions']
        self.oauth2_token = None
        self.oauth2_token_expires = None
        self.session_key = None
        self.uid = None

    def require_auth(self, next=None, required_permissions=None):
        args = {}
        if next:
            args['next'] = next
        if required_permissions:
            args['required_permissions'] = required_permissions
        parts = urlparse.urlparse(settings.FACEBOOK_AUTH_URL)
        query = urllib.urlencode(args)
        url = urlparse.urlunparse((
            parts.scheme,
            parts.netloc,
            parts.path,
            parts.params,
            query,
            parts.fragment,
        ))
        return HttpResponseRedirect(url)

    def get_canvas_url(self, path):
        """
        Resolve the path to use for the redirect_uri for authorization
        """
        if self.canvas_url:
            path = path.replace(self.canvas_url, '')
            return self.get_app_url(path)
        return path

    def oauth2_check_permissions(self, request, required_permissions,
                                 additional_permissions=None,
                                 fql_check=True, force_check=True):
        """
        Check for specific extended_permissions.

        If fql_check is True (default), oauth2_check_session() should be called
        first to ensure the access_token is in place and valid to make query.

        """
        has_permissions = False

        req_perms = set(required_permissions.split(','))

        cached_perms = set()
        if 'oauth2_extended_permissions' in request.session:
            cached_perms = request.session['oauth2_extended_permissions']

        # so now, fb_sig_ext_perms seems to contain the right perms (!)

        if not force_check and cached_perms and req_perms.issubset(cached_perms):
            # Note that this has the potential to be out of date!
            has_permissions = True
        elif fql_check:
            # TODO allow option to use preload FQL for this?
            perms_query = required_permissions

            # Note that we can query additional permissions that we
            # don't require.  This can be useful for optional
            # functionality (or simply for better caching)
            if additional_permissions:
                perms_query += ',' + additional_permissions

            perms_results = self.fql.query(
                    'select %s from permissions where uid=%s'
                    % (perms_query, self.uid))

            if not perms_results:
                return False

            perms_results = perms_results[0]
            actual_perms = set()
            for permission, allowed in perms_results.items():
                if allowed == 1:
                    actual_perms.add(permission)
            request.session['oauth2_extended_permissions'] = actual_perms
            has_permissions = req_perms.issubset(actual_perms)

        return has_permissions

    def oauth2_process_request(self, request):
        """
        Process a request handling oauth data.
        """
        redirect_uri = self.get_canvas_url(request.build_absolute_uri())
        logging.debug('Restoring oauth data from a saved session')
        if 'facebook' in request.session:
            self.oauth2_load_session(request.session['facebook'])
        if 'code' in request.GET:
            logging.debug('Exchanging oauth code for an access_token')
            # We've got a code from an authorisation, so convert it to a access_token
            self.oauth2_access_token(request.GET['code'], next=redirect_uri)
            return HttpResponseRedirect(redirect_uri)
        elif 'signed_request' in request.REQUEST:
            logging.debug('Loading oauth data from "signed_request"')
            self.oauth2_load_session(
                    self.validate_oauth_signed_request(request.REQUEST['signed_request']))
            return HttpResponseRedirect(request.get_full_path())
        elif 'session' in request.REQUEST:
            logging.debug('Loading oauth data from "session"')
            self.oauth2_load_session(
                    self.validate_oauth_session(request.REQUEST['session']))

    def oauth2_process_response(self, request, response):
        logging.debug('Saving oauth data to session')
        request.session['facebook'] = self.oauth2_save_session()

def require_oauth(local_prefix=None,
        required_permissions=settings.FACEBOOK_PERMS, check_permissions=None,
        force_check=True):
    """
    Decorator for Django views that requires the user to be OAuth 2.0'd.
    The FacebookMiddleware must be installed.
    Note that OAuth 2.0 does away with the app added/logged in distinction -
    it is now the case that users have now either authorised facebook users or
    not, and if they are, they may have granted the app a number of
    extended permissions - there is no lightweight/automatic login any more.

    Standard usage:
        @require_oauth()
        def some_view(request):
            ...
    """
    @decorator.decorator
    def newview(view, request, *args, **kwargs):
        try:
            fb = request.facebook
            redirect_uri = request.build_absolute_uri()
            valid_token = fb.oauth2_check_session(request)
            if valid_token and required_permissions:
                has_permissions = fb.oauth2_check_permissions(
                    request, required_permissions, check_permissions,
                    valid_token, force_check)
            else:
                has_permissions = True
            if not valid_token or not has_permissions:
                return fb.require_auth(next=redirect_uri,
                        required_permissions=required_permissions)
            return view(request, *args, **kwargs)
        except FacebookError as e:
            # Invalid token (I think this can happen if the user logs out)
            # Unfortunately we don't find this out until we use the api
            if e.code == 190:
                del request.session['facebook']
                return fb.require_auth(next=redirect_uri,
                        required_permissions=required_permissions)
            raise
    return newview

class FacebookMiddleware(object):
    """
    Middleware that attaches a Facebook object to every incoming request.

    canvas_url can be a string or a callable.  Using a callable lets us
    pass in something like lambda reverse('our_canvas_view') so we can follow
    the DRY principle.
    """

    def __init__(self, app_secret=None, app_name=None,
                 canvas_url=None, app_id=None,
                 oauth2=None):
        self.app_secret = app_secret or settings.FACEBOOK_APP_SECRET
        self.app_name = app_name or getattr(settings, 'FACEBOOK_APP_NAME', None)
        self.canvas_url = canvas_url or getattr(settings,
                                                'FACEBOOK_CANVAS_URL',
                                                None)
        self.app_id = app_id or getattr(settings, 'FACEBOOK_APP_ID', None)
        self.proxy = None
        if getattr(settings, 'USE_HTTP_PROXY', False):
            self.proxy = settings.HTTP_PROXY

    def process_request(self, request):
        canvas_url = self.canvas_url
        if callable(canvas_url):
            canvas_url = canvas_url()
        request.facebook = Facebook(self.app_secret, app_name=self.app_name,
                canvas_url=canvas_url, proxy=self.proxy,
                app_id=self.app_id)
        response = request.facebook.oauth2_process_request(request)
        if response:
            return response
        if 'fb_sig_session_key' in request.GET and ('fb_sig_user' in request.GET or 'fb_sig_canvas_user' in request.GET):
            request.facebook.session_key = request.session['facebook_session_key'] = request.GET['fb_sig_session_key']
            request.facebook.uid = request.session['facebook_user_id'] = request.GET['fb_sig_user'] or request.GET['fb_sig_canvas_user']
        elif int(request.GET.get('fb_sig_added', '1')) and request.session.get('facebook_session_key', None) and request.session.get('facebook_user_id', None):
            request.facebook.session_key = request.session['facebook_session_key']
            request.facebook.uid = request.session['facebook_user_id']
        elif request.facebook.oauth2_token and not request.facebook.uid:
            request.facebook.uid  = request.facebook.graph.filter('me').get()['id']

    def process_response(self, request, response):
        # Don't assume that request.facebook exists
        # - it's not necessarily true that all process_requests will have been called
        try:
            fb = request.facebook
        except AttributeError:
            return response

        fb.oauth2_process_response(request, response)

        if fb.session_key and fb.uid:
            request.session['facebook_session_key'] = fb.session_key
            request.session['facebook_user_id'] = fb.uid

            if fb.session_key_expires:
                expiry = datetime.datetime.utcfromtimestamp(fb.session_key_expires)
                request.session.set_expiry(expiry)

        return response
