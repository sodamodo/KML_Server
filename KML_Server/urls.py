from django.conf.urls import patterns, include, url
from django.contrib import admin

import os
from NetworkLink.views import path

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'NetworkLink.views.path', name='download'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
