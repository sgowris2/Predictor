__author__ = 'sudeep'
from django.conf.urls import patterns, url
from predictor import views

urlpatterns = patterns('',
    url(r'^predict/$', views.predict, name='predict'),
    url(r'^gameweek/(?P<gameweek>\w{0,50})/$', views.gameweek, name='gameweek'),
    url(r'^404/$', views.error404, name='404'),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'predictor/index.html'})
)