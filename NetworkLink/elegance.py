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
from KML_Server.settings import BASE_DIR

# KML_HOLDER = os.path.join(BASE_DIR)


Point = namedtuple('Point', ['name', 'lat', 'long', 'data'])

def placemark(row):
    # for i in range(len(row.name)):
    #     print i


    placemark = Element('Placemark')
    treeElement = ElementTree(placemark)
    name = Element('name')

        ##data test##

    extended_data = Element('ExtendedData')
    # data = Element('Data', name="holeNumber")

    displayname = Element('displayName')
    displayname.text = "Hiiiii!"
    # name = Element('name')
    name.text = row[0]



    streamtitle = Element('Data', name="Rivername")
    streamflow = Element('Data', name="Stream Flow")
    streamtitle.text = "{}".format(row.name)
    # streamtitle.text = row.data[3]
    extended_data.append(streamtitle)
    # extended_data.append(streamtitle)

    # flow_name = Element('value')
    # flow_name.text = row.data[0]
    #
    # name_name = Element('value')
    # name_name.text = row.data[0]
    #
    # flow_name.append(value)


    # description = Element('description')
    point = Element('Point')
    coordinates = SubElement(point, "coordinates")
    coordinates.text = '{},{}'.format(row.long, row.lat)

    # description.text = "Attached to the ground. Intelligently places itself at the height of the underlying terrain"

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

    # print tostring(kml)

    # range(len(makelists()[0]))

    rows = makelists()

    kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    # kml.text = "DocTest"
    document = Element("Document")
    kml.append(document)

    # print("ROWS")
    name = Element("name")
    name.text = "Guaging Stations"
    document.append(name)

    for row in rows:
        # print row.name, row.lat, row.long, row.data
        document.append(placemark(row))
        # print(tostring((document)))
        break

    print tostring(kml, pretty_print=True)


    f.write(tostring(os.path.join(BASE_DIR, 'KML', kml)))
    f.close()
    print "done!"


    return serve(request, )

#
# filepath = 'C:\Users\Def\Documents\KML_Server\KML_Server\NetworkLink\teh_kml.kml'

