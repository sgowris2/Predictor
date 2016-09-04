__author__ = 'sudeep'
from django.conf.urls import patterns, url
from predictor import views

urlpatterns = patterns('',
    url(r'^home/$', views.home, name='home'),
    url(r'^predict/$', views.predict, name='predict'),
    url(r'^gameweek/(?P<gameweek>\w{0,50})/$', views.gameweek, name='gameweek'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^about/$', views.about, name='about'),
    url(r'^404/$', views.error404, name='404'),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'predictor/index.html'})
)