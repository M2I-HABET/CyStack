#############################################################
#
#	Property of HABET.
#
#   Authors:
#           Jared Danner
#
#############################################################

import urllib.request
from io import StringIO


google_api_key = "&key=AIzaSyBPC7y0fIjsbz61P16wTudIrkfKK0Unzd4"
url_base = "https://maps.googleapis.com/maps/api/staticmap?center="
zoom_base = "&zoom="
size_base = "&size="
maptype_base = "&maptype="
marker_base = "&markers="
howe_hall_lat = "42.026695"
howe_hall_lng = "-93.653384"


def generate_map(latitude, longitude):
    """
    Oversees the process of interacting with Google Maps API, populating 
    a requested map image with the lat & lng provided, and returning a static image
    to be placed in the Tkinter GUI.
    
    @param latitude - Latitude value to mark on the map image.
    @param longitude - Longitude value to mark on the map image.
    """

    map_request = None
    map_request = url_base + str(41.7271485) + "," + str(-93.283195)
    map_request +=  zoom_base + str(9)
    map_request +=  size_base + "500x500"
    map_request +=  maptype_base + "roadmap"
    map_request +=  marker_base + "color:red%7Clabel:H%7C" + howe_hall_lat + "," + howe_hall_lng
    map_request +=  marker_base + "color:blue%7Clabel:P%7C" + str(41.427602) + "," + str(-92.913006)
    map_request +=  google_api_key

    urllib.request.urlretrieve(map_request, "gui_maps/payload_map" + "." + "jpeg")