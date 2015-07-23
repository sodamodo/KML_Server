import xml.etree.ElementTree as etree
from lxml.etree import ElementTree, Element, SubElement, tostring
from xml.dom import minidom
import csv
from bs4 import BeautifulSoup
import requests
import csv
from collections import defaultdict

def placemark(row, i):


    placemark = Element('Placemark', id=str(i))
    treeElement = ElementTree(placemark)
    name = Element('name')
    description = Element('description')
    point = Element('Point')
    coordinates = SubElement(point, "coordinates")
    # name.text = row[0]
    description.text = "Attached to the ground. Intelligently places itself at the height of the underlying terrain"
    coordinates.text = '{},{}'.format(row[2], row[1])
    placemark.append(name)
    placemark.append(description)
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

    return nameform, latform, lonform, values

# print makelists()
print "Hiiii!"

data = makelists()


collection = [[data[0], data[1], data[2], data[3]]]

names = data[0]
lat = data[1]
lon = data[2]
val = data[3]

print len(val)

for i in len(val)+1:
    print val[i][0], val[i][1], val[i][2], val[i][3]


# lat =
# print names

# for i in range(len(names)):
#     print len(names)
#     print names[i]

# , datavalues[0][0], datavalues[0][0], datavalues[0][0]
# print len(names)



# aggregated = []
# for i in range(0, len(makelists())):
#     aggregated.append([makelists()[0], makelists()[1], makelists()[2], makelists()[3]])
#     print aggregated[i]
    # writer.writerow(aggregated[i])




#
# data_dict = defaultdict(list)
# for i in xrange(0, len(aggregated)):
#     for k, v in (('name', aggregated[i][0]), ('latitude', aggregated[i][1]), ('longitude', aggregated[i][2]), ('value', aggregated[i][3])):
#         data_dict[k].append(v)