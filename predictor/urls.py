__author__ = 'sudeep'

from django.conf.urls import patterns, url
from predictor import views


urlpatterns = patterns('',
    url(r'^home/$', views.home, name='home'),
    url(r'^predict/$', views.predict, name='predict'),
    url(r'^gameweek/(?P<gameweek>\w{0,50})/$', views.gameweek, name='gameweek'),
    url(r'^gameweeks/$', views.gameweeks, name='gameweeks'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/predictor/'}),
    url(r'^register/$', views.register, name='register'),
)