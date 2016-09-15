from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('predictor.urls')),
    url(r'^predictor/', include('predictor.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
