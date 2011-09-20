from django.views.generic.simple import direct_to_template

def facebook_auth(request, template_name='fbkit/auth.html'):
    next = request.REQUEST.get('next', None)
    required_permissions = request.REQUEST.get('required_permissions', None)
    url = request.facebook.get_login_url(next=next,
            required_permissions=required_permissions)
    return direct_to_template(request, template_name, {
        'facebook_url': url,
    })

