import requests
import json

def loc(locations,price):
	url_pubs = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
	params_pubs = {'key' : 'AIzaSyA6zIAya7DpOz8KKAKTr65tw6LNI5ktKzE',
	     'location' :  location,
	       'rankby' : 'distance',
	        'type'  : 'pub',
	     'keyword'  : 'pubs',
	     'maxprice' : price
	         }
	r = requests.get(url = url_pubs, params = params_pubs)
	data = r.json()
	restaurant_name = data['resluts'][0]['name']
	lat = data['results'][0]['geometry']['location']['lat']
	lng = data['results'][0]['geometry']['location']['lng']
	map_url = "maps.google.com/?q="+str(lat)+','+str(lng)
