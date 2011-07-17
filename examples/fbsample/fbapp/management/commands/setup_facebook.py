# - coding: utf-8 -
import datetime
import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from facebook.djangofb import Facebook
from ...views import fb_callback

class Command(BaseCommand):
    def handle(self, *args, **options):
        secret_key = settings.FACEBOOK_APP_SECRET
        app_name = getattr(settings, 'FACEBOOK_APP_NAME', None)
        callback_path = getattr(settings, 'FACEBOOK_CALLBACK_PATH', None)
        app_id = getattr(settings, 'FACEBOOK_APP_ID', None)
        oauth2 = getattr(settings, 'FACEBOOK_OAUTH2', False)
        proxy = None
        if getattr(settings, 'USE_HTTP_PROXY', False):
            proxy = settings.HTTP_PROXY
        facebook = Facebook(app_secret, app_name=app_name,
                callback_path=callback_path, proxy=proxy, app_id=app_id,
                oauth2=oauth2)
        app_token = facebook.graph.get_app_access_token()
        subscriptions = facebook.graph.filter(app_id).filter('subscriptions')
        subscriptions.delete(access_token=app_token)
        subscriptions.post({
            'object': 'user',
            'fields': ['work'],
            'callback_url': urlparse.urljoin(settings.SITE_URL, reverse(fb_callback)),
            'verify_token': fb_callback.token,
        }, access_token=app_token)
