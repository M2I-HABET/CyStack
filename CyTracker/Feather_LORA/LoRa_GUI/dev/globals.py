#############################################################
#
#	Property of HABET.
#
#   Authors:
#           Jared Danner
#
#############################################################

# System user id.
SYSTEM_USER = None

# Serial port objects. Object class defined at bottom of communication.py.
# If let None, it will dynamically find its correct port #.
PORT_MISSION_CONTROL_LORA = None
PORT_PAYLOAD_LORA = None
PORT_RECOVERY_LORA = None
PORT_ROTOR_CONTROLLER = None

# Node ID's.
NODE_MISSION_CONTROL_ID = 0
NODE_PAYLOAD_ID = 1
NODE_RECOVERY_ID = 2

# Tkinter frame objects.
mc_class_reference = None
payload_class_reference = None

# Threaded timer objects.
timer_mission_control_lora = None
timer_payload_lora = None
timer_recovery_lora = None
timer_mission_control_contact_timer = None
timer_payload_contact_timer = None
timer_recovery_contact_timer = None