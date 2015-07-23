from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from NetworkLink import getpoints


import os
from NetworkLink.views import path



urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'NetworkLink.views.getpoints', name='getpoints'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
