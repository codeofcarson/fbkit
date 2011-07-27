from django.db import models

def _2int(d, k):
    try:
        d = d.__dict__
    except:
        pass
    
    t = d.get(k, '')
    if t == 'None':
        t = 0
    else:
        t = int(t)
    return t

class UserManager(models.Manager):
    """Custom manager for a Facebook User."""
    
    def get_current(self, request):
        """Gets a User object for the logged-in Facebook user."""
        facebook = request.facebook
        user, created = self.get_or_create(id=_2int(facebook, 'uid'))
        if created:
            # we could do some custom actions for new users here...
            pass
        return user

class User(models.Model):
    """A simple User model for Facebook users."""

    # Use the user's UID as the primary key in our database.
    id = models.BigIntegerField(primary_key=True)

    # The data that you want to store for each user would go here.
    # For this sample, we let users let people know their favorite progamming
    # language, in the spirit of Extended Info.
    language = models.CharField(max_length=64, default='Python')

    # Add the custom manager
    objects = UserManager()

    def __unicode__(self):
        return u'%s' % self.id
