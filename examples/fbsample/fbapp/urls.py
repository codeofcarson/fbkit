from django.conf.urls.defaults import patterns

urlpatterns = patterns('fbsample.fbapp.views',
    (r'^$', 'canvas'),
    # Define other pages you want to create here
)

