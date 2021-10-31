import requests
import urllib.parse
adress = "Чебоксары+улица+Советская+50А" #город+улица+дом
adress = urllib.parse.quote_plus(adress)
req = "https://nominatim.openstreetmap.org/?addressdetails=1&q={}&format=json&limit=1".format(adress)
req = requests.get(req).json()
req = req[0]
print(req['lat'], req['lon'])