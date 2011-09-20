from django.template.response import TemplateResponse

# Import the Django helpers
import fbkit.djangokit as facebook

# The User model defined in models.py
from .models import User

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

    # User is guaranteed to be logged in, so pass canvas.html
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    return TemplateResponse(request, 'canvas.html', {'fbuser': user})
