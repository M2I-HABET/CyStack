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
from tkinter import *
from tkinter.ttk import *


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
            urllib.request.urlretrieve(url, "gui_maps/payload_map" + "." + "PNG")
            # Configures the big picture map. (containing all nodes in 1 map).
            url = build_url_network()
            # Pulls down the configured Static Maps image from Google.
            urllib.request.urlretrieve(url, "gui_maps/network_map" + "." + "PNG")
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
            urllib.request.urlretrieve(url, "gui_maps/recovery_map" + "." + "PNG")
            # Configures the big picture map. (containing all nodes in 1 map).
            url = build_url_network()
            # Pulls down the configured Static Maps image from Google.
            urllib.request.urlretrieve(url, "gui_maps/network_map" + "." + "PNG")
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
    This image holds all nodes in the network.
    """

    # Seperates all latitude and longitude values from pairs into individual variables.
    p_lat, p_lng = previous_payload_coords.split(",")
    r_lat, r_lng = previous_recovery_coords.split(",")
    mc_lat, mc_lng = howe_hall_coords.split(",")

    # Calculates the center latitude value.
    center_lat = (float(p_lat) + float(r_lat) + float(mc_lat)) / 3.0
    center_lng = (float(p_lng) + float(r_lng) + float(mc_lng)) / 3.0

    map_center = str(center_lat) + "," + str(center_lng)

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
    

def place_payload(mc_frame):
    """
    Replaces the payload map w/ the updated one.

    @param mc_frame - Reference object that holds the payload_map_image object.
    """

    # Removes old image from GUI. Prevents stacking which may lead to crashing.
    mc_frame.payload_map_image.grid_forget()
    # Pulls Static Maps image into python.
    temp_image = PhotoImage(file="gui_maps/payload_map.png")
    # Binds image inside of label object. (Needed to use the grid layout)
    mc_frame.payload_map_image = Label(mc_frame, image=temp_image)
    # Reassigns the label object with the image attribute.
    mc_frame.payload_map_image.image = temp_image
    # Places image into GUI.
    mc_frame.payload_map_image.grid(row=16, column=0, rowspan=2, columnspan=3, sticky='nswe')


def place_recovery(mc_frame):
    """
    Replaces the recovery map w/ the updated one.

    @param mc_frame - Reference object that holds the recovery_map_image object.
    """

    # Removes old image from GUI. Prevents stacking which may lead to crashing.
    mc_frame.recovery_map_image.grid_forget()
    # Pulls Static Maps image into python.
    temp_image = PhotoImage(file="gui_maps/recovery_map.png")
    # Binds image inside of label object. (Needed to use the grid layout)
    mc_frame.recovery_map_image = Label(mc_frame, image=temp_image)
    # Reassigns the label object with the image attribute.
    mc_frame.recovery_map_image.image = temp_image
    # Places image into GUI.
    mc_frame.recovery_map_image.grid(row=16, column=5, rowspan=2, columnspan=3, sticky='nswe')


def place_network(mc_frame):
    """
    Replaces the network map w/ the updated one.

    @param mc_frame - Reference object that holds the network_map_image object.
    """

    # Removes old image from GUI. Prevents stacking which may lead to crashing.
    mc_frame.network_map_image.grid_forget()
    # Pulls Static Maps image into python.
    temp_image = PhotoImage(file="gui_maps/network_map.png")
    # Binds image inside of label object. (Needed to use the grid layout)
    mc_frame.network_map_image = Label(mc_frame, image=temp_image)
    # Reassigns the label object with the image attribute.
    mc_frame.network_map_image.image = temp_image
    # Places image into GUI.
    mc_frame.network_map_image.grid(row=16, column=9, rowspan=2, columnspan=3, sticky='nswe')