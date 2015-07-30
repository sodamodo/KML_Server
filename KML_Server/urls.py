from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from NetworkLink import views

import os



urlpatterns = patterns('',
    # Examples:
    url(r'fire', 'NetworkLink.views.fire', name='fire'),
    # url(r'update', 'NetworkLink.views.update', name='update'),
    # (r'^kml/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'welcome', 'NetworkLink.views.welcome', name='welcome'),
    # url(r'welcome', 'NetworkLink.views.gather', name='gather'),




    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


