from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
#uncomment the following two lines and the one below
#if you dont want to use a decorator instead of the middleware
#from django.utils.decorators import decorator_from_middleware
#from facebook.djangofb import FacebookMiddleware

# Import the Django helpers
import facebook.djangofb as facebook
from facebook import graph

# The User model defined in models.py
from models import User

# We'll require login for our canvas page. This
# isn't necessarily a good idea, as we might want
# to let users see the page without granting our app
# access to their info. See the wiki for details on how
# to do this.

@facebook.require_oauth()
def canvas(request):
    # Get the User object for the currently logged in user
    user = User.objects.get_current(request)

    # Check if we were POSTed the user's new language of choice
    if 'language' in request.POST:
        user.language = request.POST['language'][:64]
        user.save()

    # User is guaranteed to be logged in, so pass canvas.fbml
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    return direct_to_template(request, 'canvas.fbml', extra_context={'fbuser': user})

@facebook.require_oauth()
def ajax(request):
    return HttpResponse('hello world')

#This is callback function called by facebook during subscription process
#(look into management/commands/setup_facebook.py)
@graph.subscription_callback('testingcallback')
def subscription_callback(request, data):
    pass
