__author__ = 'sudeep'
from django.conf.urls import patterns, url
from predictor import views

urlpatterns = patterns('',
    url(r'^currentgameweek/$', views.current_gameweek, name='current_gameweek'),
    url(r'^$', 'django.contrib.auth.views.login', {
    'template_name': 'predictor/index.html'
    })
)