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
howe_hall_coords = "42.026695,-93.653384"
# Used to compare previous map's coordinate to new coordinates to prevent
# requesting the exact same map from Google's API.
previous_payload_coords = None
previous_recovery_coords = None


def generate_map(latitude, longitude, node):
    """
    Oversees the process of interacting with Google Maps API, populating 
    a requested map image with the lat & lng provided, and returning a static image
    to be placed in the Tkinter GUI.
    
    @param latitude - Latitude value to mark on the map image.
    @param longitude - Longitude value to mark on the map image.
    @param node - Payload or Recovery
    """

    # Combines the given lat & lng.
    map_center = str(latitude) + "," + str(longitude)    
    
    # Check for payload.
    if "payload" in node:
        # Check if the "new" coordinates are the same as last time.
        # Prevents duplicate map calls from the API.
        if map_center is not previous_payload_coords:
            # Update previous value.
            previous_payload_coords = map_center
            # Configures the Url needed to get the correct map from Google.
            url = build_url_payload(map_center)
            # Pulls down the configured Static Maps image from Google.
            urllib.request.urlretrieve(url, "gui_maps/payload_map" + "." + "jpeg")
            # Configures the big picture map. (containing all nodes in 1 map).
            url = build_url_network()
            # Pulls down the configured Static Maps image from Google.
            urllib.request.urlretrieve(url, "gui_maps/network_map" + "." + "jpeg")
            # New map has been generated. Replace the current image.
            return True
        # A map with this configuration has already been generated.
        # Return false to tell the software to not replace the current image.
        else:
            return False
    # Check for recovery.
    elif "recovery" in node:
        # Check if the "new" coordinates are the same as last time.
        # Prevents duplicate map calls from the API.
        if map_center is not previous_recovery_coords:
            # Update previous value.
            previous_recovery_coords = map_center
            # Configures the Url needed to get the correct map from Google.
            url = build_url_recovery(map_center)
            # Pulls down the configured Static Maps image from Google.
            urllib.request.urlretrieve(url, "gui_maps/recovery_map" + "." + "jpeg")
            # Configures the big picture map. (containing all nodes in 1 map).
            url = build_url_network()
            # Pulls down the configured Static Maps image from Google.
            urllib.request.urlretrieve(url, "gui_maps/network_map" + "." + "jpeg")
            # New map has been generated. Replace the current image.
            return True
        # A map with this configuration has already been generated.
        # Return false to tell the software to not replace the current image.
        else:
            return False


def build_url_payload(map_center):
    """ 
    Builds the required url to request the desired image from Google.
    
    @param map_cetner - Center of the map (gps coordinates)
    """

    # Builds the url to request a specific image.
    map_url = None
    map_url = url_base + map_center
    map_url +=  zoom_base + str(9)
    map_url +=  size_base + "500x500"
    map_url +=  maptype_base + "roadmap"
    map_url +=  marker_base + "color:red%7Clabel:P%7C" + map_center
    map_url +=  google_api_key
    # Returns url.
    return map_url


def build_url_recovery(map_center):
    """ 
    Builds the required url to request the desired image from Google.
    
    @param map_cetner - Center of the map (gps coordinates)
    """

    # Builds the url to request a specific image.
    map_url = None
    map_url = url_base + map_center
    map_url +=  zoom_base + str(9)
    map_url +=  size_base + "500x500"
    map_url +=  maptype_base + "roadmap"
    map_url +=  marker_base + "color:green%7Clabel:R%7C" + map_center
    map_url +=  google_api_key
    # Returns url.
    return map_url


def build_url_network():
    """ 
    Builds the required url to request the desired image from Google.
    
    @param map_cetner - 
    """


    # Builds the url to request a specific image.
    map_url = None
    map_url = url_base + map_center
    map_url +=  zoom_base + str(9)
    map_url +=  size_base + "500x500"
    map_url +=  maptype_base + "roadmap"
    map_url +=  marker_base + "color:green%7Clabel:R%7C" + map_center
    map_url +=  google_api_key
    # Returns url.
    return map_url
    
