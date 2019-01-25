#############################################################
#
#	Property of HABET.
#
#   Authors:
#           Jared Danner
#
#############################################################

# Serial port objects. Object class defined at bottom of communication.py.
PORT_MISSION_CONTROL_LORA = None
PORT_PAYLOAD_LORA = None

# Node ID's.
NODE_MISSION_CONTROL_ID = 0
NODE_PAYLOAD_ID = 1
NODE_RECOVERY_ID = 2

# Tkinter frame objects.
mc_class_reference = None

# Threaded timer objects.
timer_mission_control_lora = None
timer_payload_lora = None