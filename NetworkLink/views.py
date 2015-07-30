from KML_Server.settings import BASE_DIR
import xml.etree.ElementTree as etree
from lxml.etree import ElementTree, Element, SubElement, tostring
from xml.dom import minidom
import csv
from bs4 import BeautifulSoup
import requests
import csv
from collections import defaultdict, namedtuple
from django.views.static import serve
from KML_Server import settings
import os
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
import NetworkLink
from django.shortcuts import render

# KML_HOLDER = os.path.join(BASE_DIR)


Point = namedtuple('Point', ['name', 'lat', 'long', 'data'])
# Point = namedtuple('Point', ['name', 'lat', 'long', 'data'])


def placemark(row):

    placemark = Element('Placemark', targetId="ID")
    name = Element('name')
    extended_data = Element('ExtendedData')



    streamtitle = Element('Data', name="Rivername")
    streamflow = Element('Data', name="Stream Flow")
    streamtitle.text = "{}".format(row.name)
    streamflow.text = "{}".format(str(row.data))
    extended_data.append(streamtitle)
    extended_data.append(streamflow)

    point = Element('Point')
    # coordinates = SubElement(point, "coordinates")
    coordinates = Element('coordinates')
    coordinates.text = '{},{}'.format(row.long, row.lat)
    point.append(coordinates)


    # placemark.append(name)
    # placemark.append(description)
    placemark.append(extended_data)
    placemark.append(point)



    ##Styling information
    style = Element("Style", id="ID")
    iconstyle = Element('IconStyle', id="ID")
    scale = Element('scale')
    iconstyle.append(scale)
    style.append(iconstyle)
    placemark.append(style)
    icon = Element("Icon")
    iconstyle.append(icon)
    href = Element("href")
    href.text = "http://maps.google.com/mapfiles/kml/paddle/purple-circle.png"
    icon.append(href)
    color = Element('color')
    iconstyle.append(color)
    color.text = '50DC783C'

    return placemark



def makelists():
    r = requests.get('http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&indent=on&stateCd=ga&parameterCd=00060,00065&siteType=ST')

    soup = BeautifulSoup(r.text, "lxml-xml")

    names = []
    for r in soup.find_all("siteName"):
        names.append(r.contents)



    latitude = []
    for lat in soup.find_all("latitude"):
        latitude.append(lat.contents)

    longitude = []
    for lon in soup.find_all("longitude"):
        longitude.append(lon.contents)


    values = []
    for v in soup.find_all("value"):
        values.append(v.contents)

    #formatted data begins here
    nameform = []
    for name in names:
        nameform.append(name[0])

    latform = []
    for lat in latitude:
        latform.append(float(lat[0]))

    lonform = []
    for lon in longitude:
        lonform.append(float(lon[0]))


    valform = []
    for val in values:
        valform.append(float(val[0]))

    data = zip(nameform, latform, lonform, values)
    points = [Point(*point) for point in data]
    # points = [Point(name, lat, long, data) for name, lat, long ,data in data]


    return points


def fire(request):



    kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    document = Element("Document")
    document.text = "doooz" # d'elete later
    kml.append(document)
    rows = makelists()



    # print("ROWS")
    name = Element("name")
    name.text = "Guaging Stations"
    document.append(name)
    # folder = Element("Folder")

    for row in rows:
        document.append(placemark(row))
        continue

    placemark_list = []
    # for row in rows:
    #     # placemark_list.append()
    #     # document.append(placemark(row))
    #     placemark(row)

    print tostring(kml, pretty_print=True)


    # f = open(os.path.join(BASE_DIR, 'NetworkLink', 'static', 'NetworkLink', 'guages.kml'), 'wb')
    # f.write(tostring(kml))
    # f.write(tostring(os.path.join('KML_Server', 'static')))
    # f.close()


    return HttpResponse(tostring(kml))
    # print "done!"
    # # #
    # downloadfile = open('gauges.kml', 'rb')
    #
    #
    # response = HttpResponse(FileWrapper(downloadfile), content_type='application/vnd.google-earth.kml+mlml;')
    # response['Content-Disposition'] = 'attachment; kml.kml'  # make custom download name
    # return response
            # return HttpResponseRedirect(reverse('fly.views.upload'))

def welcome(request):
    return render(request, 'Welcome.html')