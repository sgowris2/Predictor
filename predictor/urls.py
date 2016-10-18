__author__ = 'sudeep'

from django.conf.urls import url
from django.contrib.auth.views import logout
from predictor import views


urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^predict/$', views.predict, name='predict'),
    url(r'^gameweek/(?P<gameweek>\w{0,50})/$', views.gameweek, name='gameweek'),
    url(r'^gameweek/(?P<gameweek>\w{0,50})/(?P<username>[-\w.]+)/$', views.gameweek, name='gameweek'),
    url(r'^gameweeks/$', views.gameweeks, name='gameweeks'),
    url(r'^gameweeks/(?P<username>[-\w.]+)/$', views.gameweeks, name='gameweeks'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact_success/$', views.contact_success, name='contact_success'),
    url(r'^contact_timeout/$', views.contact_timeout, name='contact_timeout'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/predictor/'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^already_logged_in/$', views.already_logged_in, name='already_logged_in'),
]