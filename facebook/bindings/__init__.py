from .. import proxies

from . import (
    admin, application, auth, comments, connect, dashboard, data, events, fbml,
    feed, fql, friends, groups, links, livemessage, marketplace, notifications,
    pages, photos, profile, sms, status, stream, users, update, video,
)

PROXIES = {
    'admin': admin.Proxy,
    'application': application.Proxy,
    'auth': auth.Proxy,
    'comments': comments.Proxy,
    'connect': connect.Proxy,
    'dashboard': dashboard.Proxy,
    'data': data.Proxy,
    'events': events.Proxy,
    'fbml': fbml.Proxy,
    'feed': feed.Proxy,
    'fql': fql.Proxy,
    'friends': friends.Proxy,
    'groups': groups.Proxy,
    'links': links.Proxy,
    'livemessage': livemessage.Proxy,
    'marketplace': marketplace.Proxy,
    'notifications': notifications.Proxy,
    'pages': pages.Proxy,
    'photos': photos.Proxy,
    'profile': profile.Proxy,
    'sms': sms.Proxy,
    'status': status.Proxy,
    'stream': stream.Proxy,
    'users': users.Proxy,
    'update': update.Proxy,
    'video': video.Proxy,
}
