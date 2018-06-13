import gmplot
import pandas
import requests
import googlemaps
import gmaps


df = pandas.read_csv("..//misc_projects/countries.csv")
cities = df.dropna(axis=0)
good_columns = cities._get_numeric_data()


lats = []
lons = []
for x in cities["latitude"]:
    lats.append(x)

for y in cities["longitude"]:
    lons.append(y)

z = zip(lats, lons)

google_maps_api_key = 'AIzaSyDPlspd1iebBmVGRUH3DYTwJEtjzLjZ3Yc'
gmaps = googlemaps.Client(key=google_maps_api_key)
for city in z:
    print city
    gmaps.reverse_geocode(lat)
    url ='https://maps.googleapis.com/maps/api/geocode/json?address={}&amp;key={}'\
         .format(city, google_maps_api_key)
    r = requests.get(url).json()
    lat = r['results'][0]['geometry']['location']['lat']
    lng = r['results'][0]['geometry']['location']['lng']
    lats.append(lat)
    lons.append(lng)
    # print city, gmaps.reverse_geocode((lat, lng))

gmap = gmplot.GoogleMapPlotter(0, 0, 2)
gmap.heatmap(lats, lons)
# gmap.plot(lats, lons)
gmap.scatter(lats, lons, c='r', marker=True)
gmap.draw("countries.html")

