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





pointsfile = open('kml_points.kml', 'wb')
f = open("raw_points.csv", 'rt')
print(f)


kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
document = Element("Document")
kml.append(document)



i = 0
for row in f:
    i += 1
    document.append(placemark(row, i))

f.close()


kmlstring = tostring(kml)
# print kmlstring
print(tostring(kml, pretty_print=True))
# pointsfile.write(kmlstring)
# pointsfile.close()
print "done!"





