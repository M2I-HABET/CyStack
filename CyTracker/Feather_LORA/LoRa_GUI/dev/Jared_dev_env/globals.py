#############################################################
#
#	Property of Eagle Eye. 
#
#   Authors:
#           Jared Danner
#
#############################################################

# Serial port objects. Object class defined at bottom of communication.py. 
PORT_MC_LORA = None
PORT_CRAFT_LORA = None
PORT_CRAFT_MEGA = None

# Node ID's.
NODE_MISSION_CONTROL_ID = 0
NODE_EAGLE_EYE_ID = 1
NODE_RELAY_ID = 2

# Tkinter frame objects.
mc_class_reference = None

# Threaded timer objects.
timer_mc_lora = None
timer_craft_lora = None
timer_craft_mega = None
# timer_xbox_controller = None