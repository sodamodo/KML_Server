from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import os
from django.conf import settings
from django.core.servers.basehttp import FileWrapper


# Create your views here.

def path(request):
    load_path = os.path.join(settings.BASE_DIR, "NetworkLink", "points.kml")

    downloadfile = open(load_path, 'rb')

    response = HttpResponse(FileWrapper(downloadfile), content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename=loader.kml'  # make custom download name
    return response