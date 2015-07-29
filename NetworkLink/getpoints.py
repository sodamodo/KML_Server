from bs4 import BeautifulSoup
import requests
import csv
from collections import defaultdict




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

nameform = []
for name in names:
    nameform.append(name[0].encode("utf-8"))

latform = []
for lat in latitude:
    latform.append(float(lat[0]))

lonform = []
for lon in longitude:
    lonform.append(float(lon[0]))


valform = []
for val in values:
    valform.append(float(val[0]))



f = open('raw_points.csv', 'wb')

# writer = csv.DictWriter(open('points.csv', 'w'), delimiter=',', lineterminator='\n', fieldnames=['name', 'latitude', 'longitude', 'value'], extrasaction='ignore')
# writer = csv.writer('points.csv', 'wb')
writer = csv.writer(f)
# writer.writerow(('name', 'latitude', 'longitude', 'value'))

aggregated = []
for i in xrange(0, len(nameform)):
    aggregated.append([names[i][0], float(latitude[i][0]), float(longitude[i][0]), float(values[i][0])])
    # print aggregated[i]
    # writer.writerow(aggregated[i])

data_dict = defaultdict(list)
for i in xrange(0, len(aggregated)):
    for k, v in (('name', aggregated[i][0]), ('latitude', aggregated[i][1]), ('longitude', aggregated[i][2]), ('value', aggregated[i][3])):
        data_dict[k].append(v)


# print data_dict.get('latitude')

name = data_dict.get('name')
latitude = data_dict.get('latitude')
longitude = data_dict.get('longitude')
value = data_dict.get('value')
# print value

raw_data = []
for i in xrange(0, len(aggregated)):
    # raw_data.append("{}, {}, {}, {}".format([name[i], latitude[i], longitude[i], value[i]]))
    writer.writerow((name[i], latitude[i], longitude[i], value[i]))
    # raw_data.append([name[i], latitude[i], longitude[i], value[i]])
    # writer.writerow("{}, {}, {}, {}".format(name[i], latitude[i], longitude[i], value[i]))
print raw_data
# print(data_dict)

f.close()



# print aggregated
