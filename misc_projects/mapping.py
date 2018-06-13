import gmplot
import pandas
import requests
import googlemaps


df = pandas.read_csv("..//misc_projects/utah_cities.csv")
grouped_city_df = df.groupby('City').agg({'City': lambda x: len(x.unique())}).sort_values(by='City', ascending=False)
google_maps_api_key = 'AIzaSyDPlspd1iebBmVGRUH3DYTwJEtjzLjZ3Yc'
cities = grouped_city_df.index
gmaps = googlemaps.Client(key=google_maps_api_key)
lats = []
lons = []
for city in cities:
    print city
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
gmap.draw("utah.html")