import requests, os
# from dotenv import load_dotenv

REQ = f"""https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer?f=json&token=AAPKe5c31dd360d44276879b5b6091cfc366Fe_uh1BFTpmqu_CuZvwwZtUotTX4cI-ZXDH5y3VnGt5doAzGKx_38GdB_D8XaH4C&"""
print(REQ)
data = requests.post(REQ)
print(data.text)
print(data.json)