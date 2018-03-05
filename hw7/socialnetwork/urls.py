from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Menu
    url(r'^$', views.home, name='home'),
    url(r'^post', views.post, name='post'),
    url(r'^follower$', views.follower, name='follower'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^editProfile$', views.edit, name='edit'),
    url(r'^photo/(?P<username>\w+)$', views.get_photo, name='photo'),
    url(r'^unfollow/(?P<username>\w+)$', views.unfollow, name='unfollow'),
    url(r'^follow/(?P<username>\w+)$', views.follow, name='follow'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^get-list-json/(?P<time>.+)$', views.getchanges),
    url(r'^add-comment/(?P<post_id>\d+)$', views.add_comment),
    url(r'^get-comments-changes/(?P<max_pk>\d+)/(?P<post_id>\d+)$', views.get_comments_changes),
    url(r'^get-list-json-follower/(?P<username>.+)/(?P<time>.+)$', views.getchanges_follower),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),
]

