# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# import os
# from django.conf import settings
# from django.core.servers.basehttp import FileWrapper
# from KML_Server.settings import BASE_DIR
# from bs4 import BeautifulSoup
# import requests
# import csv
# from collections import defaultdict
# from django.http import HttpResponse
#
#
# # Create your views here.
#
# def getpoints(request):
#     r = requests.get('http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&indent=on&stateCd=ga&parameterCd=00060,00065&siteType=ST')
#
#     soup = BeautifulSoup(r.text, "lxml-xml")
#
#
#     names = []
#     for r in soup.find_all("siteName"):
#         names.append(r.contents)
#
#
#     latitude = []
#     for lat in soup.find_all("latitude"):
#         latitude.append(lat.contents)
#
#     longitude = []
#     for lon in soup.find_all("longitude"):
#         longitude.append(lon.contents)
#
#
#     values = []
#     for v in soup.find_all("value"):
#         values.append(v.contents)
#
#     nameform = []
#     for name in names:
#         nameform.append(name[0].encode("utf-8"))
#
#     latform = []
#     for lat in latitude:
#         latform.append(float(lat[0]))
#
#     lonform = []
#     for lon in longitude:
#         lonform.append(float(lon[0]))
#
#
#     valform = []
#     for val in values:
#         valform.append(float(val[0]))
#
#
#
#     f = open('raw_points.csv', 'wb')
#
#     # writer = csv.DictWriter(open('points.csv', 'w'), delimiter=',', lineterminator='\n', fieldnames=['name', 'latitude', 'longitude', 'value'], extrasaction='ignore')
#     # writer = csv.writer('points.csv', 'wb')
#     writer = csv.writer(f)
#     # writer.writerow(('name', 'latitude', 'longitude', 'value'))
#
#     aggregated = []
#     for i in xrange(0, len(nameform)):
#         aggregated.append([names[i][0], float(latitude[i][0]), float(longitude[i][0]), float(values[i][0])])
#         print aggregated[i]
#         # writer.writerow(aggregated[i])
#
#     data_dict = defaultdict(list)
#     for i in xrange(0, len(aggregated)):
#         for k, v in (('name', aggregated[i][0]), ('latitude', aggregated[i][1]), ('longitude', aggregated[i][2]), ('value', aggregated[i][3])):
#             data_dict[k].append(v)
#
#
#     # print data_dict.get('latitude')
#
#     name = data_dict.get('name')
#     latitude = data_dict.get('latitude')
#     longitude = data_dict.get('longitude')
#     value = data_dict.get('value')
#     # print value
#
#     raw_data = []
#     for i in xrange(0, len(aggregated)):
#         # raw_data.append("{}, {}, {}, {}".format([name[i], latitude[i], longitude[i], value[i]]))
#         writer.writerow([name[i], latitude[i], longitude[i], value[i]])
#     # raw_data.append([name[i], latitude[i], longitude[i], value[i]])
#     # writer.writerow("{}, {}, {}, {}".format(name[i], latitude[i], longitude[i], value[i]))
#     print f
#     # print(data_dict)
#
#     f.close()
#     return HttpResponse('')
#
#
# def path(request):
#     load_path = os.path.join(settings.BASE_DIR, "NetworkLink", "static", "points.kml")
#
#     downloadfile = open(load_path, 'rb')
#
#     response = HttpResponse(FileWrapper(downloadfile), content_type='application/vnd.google-earth.kml+xml')
#     response['Content-Disposition'] = 'attachment; filename=loader.kml'  # make custom download name
#     return response



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


# KML_HOLDER = os.path.join(BASE_DIR)


Point = namedtuple('Point', ['name', 'lat', 'long', 'data'])
i = 0


def placemark(row):

    placemark = Element('Placemark', targetId=str(i))
    # treeElement = ElementTree(placemark)
    name = Element('name')


    extended_data = Element('ExtendedData')
    # data = Element('Data', name="holeNumber")

    # displayname = Element('displayName')
    # displayname.text = "Hiiiii!"
    name = Element('name')
    name.text = row[0]



    streamtitle = Element('Data', name="Rivername")
    streamflow = Element('Data', name="Stream Flow")
    streamtitle.text = "{}".format(row.name)
    streamflow.text = "{}".format(row.data)
    extended_data.append(streamtitle)
    extended_data.append(streamflow)

    point = Element('Point')
    # coordinates = SubElement(point, "coordinates")
    coordinates = Element('coordinates')
    coordinates.text = '{},{}'.format(row.long, row.lat)
    point.append(coordinates)


    placemark.append(name)
    # placemark.append(description)
    placemark.append(extended_data)
    placemark.append(point)



    ##Styling information
    style = Element("Style", id="ID")
    iconstyle = Element('IconStyle', id="ID")
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
    document.text = "doooz" # delete later
    kml.append(document)

    f = open("teh_kml.kml", 'wb')

    rows = makelists()

    kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    # kml.text = "DocTest"
    document = Element("Document")
    kml.append(document)

    # print("ROWS")
    name = Element("name")
    name.text = "Guaging Stations"
    document.append(name)
    folder = Element("Folder")

    for row in rows:
        # print row.name, row.lat, row.long, row.data
        document.append(placemark(row))
        # print(tostring((document)))


    print tostring(kml, pretty_print=True)


    # f.write(tostring(os.path.join(BASE_DIR, 'KML', kml)))
    f.write(tostring(kml))
    f.close()
    print "done!"
    #
    downloadfile = open('teh_kml.kml', 'rb')


    response = HttpResponse(FileWrapper(downloadfile), content_type='application/vnd.google-earth.kml+xml;')
    response['Content-Disposition'] = 'attachment; kml.kml'  # make custom download name
    return response
            # return HttpResponseRedirect(reverse('fly.views.upload'))




#
# filepath = 'C:\Users\Def\Documents\KML_Server\KML_Server\NetworkLink\teh_kml.kml'

