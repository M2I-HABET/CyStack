#############################################################
#
#	Property of HABET.
#
#   Authors:
#           Jared Danner
#
#############################################################

from tkinter import *
from tkinter.ttk import *
from communication import *
import time
import threading
import globals as g


class Recovery_Tab():

	def __init__(self, payload_frame):
		"""
		Initialization function for the class.

		@param self     - Instance of the class.
		@param payload_frame - Where this class will place its widgets.
		"""

		# Parent variables.
		self.payload_frame = payload_frame

		# Network variables.
		self.operational_mode = None
		self.roll_call_status = None
		self.node_mission_control = None
		self.node_payload = None
		self.node_recovery = None
		self.radio_received = None
		self.radio_sent = None
		self.radio_payload_rssi = None
		self.radio_recovery_rssi = None
		self.radio_payload_last_contact = None
		self.radio_recovery_last_contact = None
		self.radio_last_received_node = None
		self.radio_received_node_id = None

		# HABET Payload variables.
		self.payload_time = None
		self.payload_altitude = None
		self.payload_latitude = None
		self.payload_longitude = None
		self.payload_event = None
		self.payload_speed = None

		# Recovery variables.
		self.recovery_time = None
		self.recovery_latitude = None
		self.recovery_longitude = None

		# Mission Control variables.
		self.mission_control_time = None
		self.payload_time_previous = ""


	def variable_setup(self):
		"""
		Initializes classe variables to proper types and starting values.

		@param self - Instance of the class.
		"""

		# StringVar variables are strings that update their text in entries when
		# their value is changed.
		self.mission_control_time = StringVar(self.payload_frame)
		self.recovery_time = StringVar(self.payload_frame)
		self.recovery_latitude = StringVar(self.payload_frame)
		self.recovery_longitude = StringVar(self.payload_frame)
		self.roll_call_status = StringVar(self.payload_frame)
		self.radio_received = StringVar(self.payload_frame)
		self.radio_sent = StringVar(self.payload_frame)
		self.radio_payload_rssi = StringVar(self.payload_frame)
		self.radio_recovery_rssi = StringVar(self.payload_frame)
		self.radio_payload_last_contact = StringVar(self.payload_frame)
		self.radio_recovery_last_contact = StringVar(self.payload_frame)
		self.radio_last_received_node = StringVar(self.payload_frame)
		self.payload_time = StringVar(self.payload_frame)
		self.payload_altitude = StringVar(self.payload_frame)
		self.payload_latitude = StringVar(self.payload_frame)
		self.payload_longitude = StringVar(self.payload_frame)
		self.payload_event = StringVar(self.payload_frame)
		self.payload_speed = StringVar(self.payload_frame)
		self.radio_received_node_id = StringVar(self.payload_frame)

		# Initialization of varaible values on GUI startup.
		self.radio_received.set("-------")
		self.radio_sent.set("-------")
		self.radio_payload_rssi.set("-------")
		self.radio_recovery_rssi.set("-------")
		self.radio_payload_last_contact.set("-------")
		self.radio_recovery_last_contact.set("-------")
		self.radio_last_received_node.set("Recovery")
		self.payload_time.set("-------")
		self.payload_altitude.set("-------")
		self.payload_latitude.set("-------")
		self.payload_longitude.set("-------")
		self.payload_event.set("-------")
		self.payload_speed.set("-------")
		self.radio_received_node_id.set("-------")
		self.mission_control_time.set("-------")
		self.recovery_time.set("-------")
		self.recovery_latitude.set("-------")
		self.recovery_longitude.set("-------")


	def create_entry_objects(self):
		"""
		Creates/configures entry objects.

		@param self - Instance of the class.
		"""

		# Creates entry widgets for each variable. (Text windows to be placed in the GUI)
		self.entry_radio_received = Entry(self.payload_frame, state="readonly", textvariable=self.radio_received, font='Helvtica 11')
		self.entry_radio_sent = Entry(self.payload_frame, state="readonly", textvariable=self.radio_sent, font='Helvtica 11')
		self.entry_radio_payload_rssi = Entry(self.payload_frame, state="readonly", textvariable=self.radio_payload_rssi, font='Helvtica 11')
		self.entry_radio_recovery_rssi = Entry(self.payload_frame, state="readonly", textvariable=self.radio_recovery_rssi, font='Helvtica 11')
		self.entry_radio_payload_last_contact = Entry(self.payload_frame, state="readonly", textvariable=self.radio_payload_last_contact, font='Helvtica 11')
		self.entry_radio_recovery_last_contact = Entry(self.payload_frame, state="readonly", textvariable=self.radio_recovery_last_contact, font='Helvtica 11')
		self.entry_payload_time = Entry(self.payload_frame, state="readonly", textvariable=self.payload_time, justify='right', font='Helvtica 11')
		self.entry_payload_altitude = Entry(self.payload_frame, state="readonly", textvariable=self.payload_altitude, justify='right', font='Helvtica 11')
		self.entry_payload_latitude = Entry(self.payload_frame, state="readonly", textvariable=self.payload_latitude, justify='right', font='Helvtica 11')
		self.entry_payload_longitude = Entry(self.payload_frame, state="readonly", textvariable=self.payload_longitude, justify='right', font='Helvtica 11')
		self.entry_payload_event = Entry(self.payload_frame, state="readonly", textvariable=self.payload_event, justify='right', font='Helvtica 11')
		self.entry_payload_speed = Entry(self.payload_frame, state="readonly", textvariable=self.payload_speed, justify='right', font='Helvtica 11')
		self.entry_radio_received_node_id = Entry(self.payload_frame, state="readonly", textvariable=self.radio_received_node_id, justify='center', font='Helvtica 11')
		self.entry_mission_control_time = Entry(self.payload_frame, state="readonly", textvariable=self.mission_control_time, justify='right', font='Helvtica 11')
		self.entry_recovery_time = Entry(self.payload_frame, state="readonly", textvariable=self.recovery_time, justify='right', font='Helvtica 11')
		self.entry_recovery_latitude = Entry(self.payload_frame, state="readonly", textvariable=self.recovery_latitude, justify='right', font='Helvtica 11')
		self.entry_recovery_longitude = Entry(self.payload_frame, state="readonly", textvariable=self.recovery_longitude, justify='right', font='Helvtica 11')
		self.entry_radio_last_received_node = Entry(self.payload_frame, state="readonly", justify='center', textvariable=self.radio_last_received_node, font='Helvetica 18 bold')


	def layout_network(self):
		"""
		Binds the sections of widgets related to the network to the top
		portion of the frame.

		@param self - Instance of the class.
		"""

		# Above divider one. (divider at bottom of method)
		self.create_label_center(1, 1, self.payload_frame, "NETWORK")
		self.create_label_east(0, 5, self.payload_frame, "Received:")
		self.entry_radio_received.grid(row=0, column=6, columnspan=14, sticky='we')
		self.create_label_east(1, 5, self.payload_frame, "Sent:")
		self.entry_radio_sent.grid(row=1, column=6, columnspan=14, stick='we')
		self.create_label_east(2, 5, self.payload_frame, "RSSI Payload:")
		self.entry_radio_payload_rssi.grid(row=2, column=6, columnspan=1, stick='we')
		self.create_label_east(2, 7, self.payload_frame, "Last Contact (s):")
		self.entry_radio_payload_last_contact.grid(row=2, column=8, columnspan=1, stick='we')
		self.create_label_east(3, 5, self.payload_frame, "RSSI Recovery:")
		self.entry_radio_recovery_rssi.grid(row=3, column=6, columnspan=1, stick='we')
		self.create_label_east(3, 7, self.payload_frame, "Last Contact (s):")
		self.entry_radio_recovery_last_contact.grid(row=3, column=8, columnspan=1, stick='we')
		self.create_label_center(2, 10, self.payload_frame, "Last Packet Received Was From")
		self.entry_radio_last_received_node.grid(row=3, column=10, rowspan=2, sticky='nsew')

		# Terminal divider. KEEP AT THE BOTTOM OF THIS METHOD.
		# This divider is a golden bar strecthing across the screen to provide
		# distinction between variable sections.
		terminal_divider_one = Label(self.payload_frame, background="#F1BE48")
		terminal_divider_one.grid(row=5, column=0, columnspan=20, sticky='we')


	def layout_nodes(self):
		"""
		Binds the sections of widgets related to the payload to the middle
		portion of the frame.

		@param self - Instance of the class.
		"""

		# PAYLOAD
		self.create_label_center(6, 1, self.payload_frame, "PAYLOAD")
		self.create_label_center(7, 0, self.payload_frame, "Up Time (s): ")
		self.entry_payload_time.grid(row=7, column=1, sticky='we')
		self.create_label_center(8, 0, self.payload_frame, "Altitude (m): ")
		self.entry_payload_altitude.grid(row=8, column=1, sticky='we')
		self.create_label_center(9, 0, self.payload_frame, "Latitude:       ")
		self.entry_payload_latitude.grid(row=9, column=1, sticky='we')
		self.create_label_center(10, 0, self.payload_frame, "Longitude:   ")
		self.entry_payload_longitude.grid(row=10, column=1, sticky='we')
		self.create_label_center(11, 0, self.payload_frame, "Event:            ")
		self.entry_payload_event.grid(row=11, column=1, sticky='we')
		self.create_label_center(12, 0, self.payload_frame, "Speed (m):       ")
		self.entry_payload_speed.grid(row=12, column=1, sticky='we')
		# RECOVERY
		self.create_label_center(6, 6, self.payload_frame, "RECOVERY")
		self.create_label_center(7, 5, self.payload_frame, "Up Time (s): ")
		self.entry_recovery_time.grid(row=7, column=6, sticky='we')
		self.create_label_center(8, 5, self.payload_frame, "Latitude:       ")
		self.entry_recovery_latitude.grid(row=8, column=6, sticky='we')
		self.create_label_center(9, 5, self.payload_frame, "Longitude:   ")
		self.entry_recovery_longitude.grid(row=9, column=6, sticky='we')
		# MISSION CONTROL
		self.create_label_center(6, 9, self.payload_frame, "MISSION CONTROL")
		self.create_label_center(7, 8, self.payload_frame, "Up Time (s):   ")
		self.entry_mission_control_time.grid(row=7, column=9, sticky='we')


		# Terminal divider. KEEP AT THE BOTTOM OF THIS METHOD.
		# This divider is a golden bar strecthing across the screen to provide
		# distinction between variable sections.
		terminal_divider_two = Label(self.payload_frame, background="#F1BE48")
		terminal_divider_two.grid(row=13, column=0, columnspan=20, sticky='we')


	def layout_updated_commands(self):
		"""
		Binds the sections of widgets related to mission_control to the bottom
		portion of the frame.

		@param self - Instance of the class.
		"""



	def populate_payload_tab(self):
		"""
		Fills the frame with widgets needed for the mission control interface.

		@param self - Instance of the class.
		"""

		# Initializes class variables.
		self.variable_setup()
		# Creates/configures the tk widgets.
		self.create_entry_objects()
		# Aligns the widgets to the frame's grid.
		self.layout_network()
		self.layout_nodes()
		self.layout_updated_commands()
		# Update class instance stored as global.
		g.payload_class_reference = self


	def callback_update_gui(self, *args):
		"""
		Method is run each time the connected microcontrollers send serial data to the gui.
		This method is triggered via a .trace() on the StringVar object .input which
		can be found near the bottom of the communication.py file.

		@param self - Instance of the class.
		@param *args - Any other random system varaible that gets passed in.
		"""

		# Ensure the memory is clear.
		temp_input = ""
		# Checks for a none null connection to mission_control microcontroller.
		if g.PORT_MISSION_CONTROL_LORA is not None:
			# If valid connection, get its serial data input.
			temp_input = g.PORT_MISSION_CONTROL_LORA.input.get()
			# Splits the serial stream into two parts. Variables & pure radio packets.
			serial_data, radio_data = str(temp_input).split("]")
			# Variables such as '$' and 'N' are thrown out as junk.
			junk, junk, p_ts, p_alt, p_lat, p_lng, p_event, p_speed, node_id, mc_ts, r_ts, r_lat, r_lng = str(serial_data).split(",")
			radio_in, radio_out, received_rssi, junk = str(radio_data).split("/")
			# Setting individual variables from the parsed packet.
			self.payload_time.set(p_ts)
			self.payload_altitude.set(p_alt)
			t_lat = (float(p_lat) / 10000)
			t_lng = (float(p_lng) / 10000)
			self.payload_latitude.set(str(t_lat))
			self.payload_longitude.set(str(t_lng))
			self.payload_event.set(p_event)
			self.payload_speed.set(p_speed)
			self.mission_control_time.set(mc_ts)
			self.recovery_time.set(r_ts)
			t_lat = (float(r_lat) / 10000)
			t_lng = (float(r_lng) / 10000)
			self.recovery_latitude.set(t_lat)
			self.recovery_longitude.set(t_lng)
			self.radio_received.set(radio_in)
			self.radio_sent.set(radio_out)
			# To retrieve the RSSI value of the last received packet, we need to parse out the radio_in
			# variable to see the node id.
			# $   p_ts  p_alt p_lat p_lng p_ev  p_sp  mc_ts r_ts  r_lat r_lng      node id                  $
			junk, junk, junk, junk, junk, junk, junk, junk, junk, junk, junk, self.radio_received_node_id, junk = str(radio_in).split(",")
			# Checks if the packet is from the payload.
			if "2.00" in self.radio_received_node_id:
				# Say you don't receive the a packet in a while. The mission control
				# LoRa still sends you its last known packet each time it tries to
				# update the gui (roughly 1.5 seconds). To prevent the gui from thinking
				# each "gui update" is brand new information, we compare a previous
				# variable value to the proclaimed to be new value. If they are the same, its most
				# likely the same packet we already saw. If they are different, its 100%
				# new.
				if self.payload_time_previous != str(self.payload_time.get()):
					# Updates the appropriate variables.
					self.payload_time_previous = str(self.payload_time.get())
					self.radio_last_received_node.set("Payload")
					self.update_payload_rssi(received_rssi)
			# Checks if the packet is from the recovery team.
			elif "3.00" in self.radio_received_node_id:
				# Say you don't receive the a packet in a while. The mission control
				# LoRa still sends you its last known packet each time it tries to
				# update the gui (roughly 1.5 seconds). To prevent the gui from thinking
				# each "gui update" is brand new information, we compare a previous
				# variable value to the proclaimed to be new value. If they are the same, its most
				# likely the same packet we already saw. If they are different, its 100%
				# new.
				if self.payload_time_previous != str(self.payload_time.get()):
					# Updates the appropriate variables.
					self.payload_time_previous = str(self.payload_time.get())
					self.radio_last_received_node.set("Recovery")
					self.update_recovery_rssi(received_rssi)



	def update_payload_rssi(self, received_rssi):
		"""
		Updates GUI's variables holding information about the last received
		payload packet.

		@param self  - Instance of the class.
		@param *args - The RSSI of the last received packet.
		"""

		# Checks if timer is already running.
		if g.timer_payload_contact_timer is not None:
			# If so, disable it to resync the 1sec timer.
			g.timer_payload_contact_timer.cancel()
		# If so, assign RSSI to the payload variables.
		self.radio_payload_rssi.set(received_rssi)
		# Reset the last contact timer.
		self.radio_payload_last_contact.set("0")
		# Creates countdown timer that, upon hitting zero runs the associated method.
		# Units are seconds.
		g.timer_payload_contact_timer = threading.Timer(1.0, self.timer_increment_payload_last_contact)
		# Starts the countdown timer.
		g.timer_payload_contact_timer.start()


	def timer_increment_payload_last_contact(self):
		"""
		Increments the payload node's last contact variable each second.
		This timer is resynced each time a packet from the payload
		is received.

		@param self  - Instance of the class.
		"""

		# Creates countdown timer that, upon hitting zero runs the associated method.
		# Units are seconds.
		g.timer_payload_contact_timer = threading.Timer(1.0, self.timer_increment_payload_last_contact)
		# Starts the countdown timer.
		g.timer_payload_contact_timer.start()
		# Increments the payload last contact timer on a 1 second interval.
		self.radio_payload_last_contact.set(str(int(self.radio_payload_last_contact.get()) + 1))


	def update_recovery_rssi(self, received_rssi):
		"""
		Updates GUI's variables holding information about the last received
		recovery packet.

		@param self  - Instance of the class.
		@param *args - The RSSI of the last received packet.
		"""

		# Checks if timer is already running.
		if g.timer_recovery_contact_timer is not None:
			# If so, disable it to resync the 1sec timer.
			g.timer_recovery_contact_timer.cancel()
		# If so, assign RSSI to the recovery variables.
		self.radio_recovery_rssi.set(received_rssi)
		# Reset the last contact timer.
		self.radio_recovery_last_contact.set("0")
		# Creates countdown timer that, upon hitting zero runs the associated method.
		# Units are seconds.
		g.timer_recovery_contact_timer = threading.Timer(1.0, self.timer_increment_recovery_last_contact)
		# Starts the countdown timer.
		g.timer_recovery_contact_timer.start()


	def timer_increment_recovery_last_contact(self):
		"""
		Increments the recovery node's last contact variable each second.
		This timer is resynced each time a packet from the payload
		is received.

		@param self  - Instance of the class.
		"""

		# Creates countdown timer that, upon hitting zero runs the associated method.
		# Units are seconds.
		g.timer_recovery_contact_timer = threading.Timer(1.0, self.timer_increment_recovery_last_contact)
		# Starts the countdown timer.
		g.timer_recovery_contact_timer.start()
		# Increments the recovery last contact timer on a 1 second interval.
		self.radio_recovery_last_contact.set(str(int(self.radio_recovery_last_contact.get()) + 1))


	def create_label_east(self, r, c, frame, title):
		"""
		Creates a label to be placed inside of the passed in frame at the given grid locations.
		@param self  - Instance of the class.
		@param r     - Row of frame.
		@param c     - Column of frame.
		@param frame - Frame to be bound to.
		@param title - String title to be assigned to the label.
		"""

		# Label object.
		label = Label(frame, text=title, font='Helvetica 12 bold')
		label.grid(row=r, column=c, sticky='e')


	def create_label_center(self, r, c, frame, title):
		"""
		Creates a label to be placed inside of the passed in frame at the given grid locations.
		@param self  - Instance of the class.
		@param r     - Row of frame.
		@param c     - Column of frame.
		@param frame - Frame to be bound to.
		@param title - String title to be assigned to the label.
		"""

		# Label object.
		label = Label(frame, text=title, font='Helvetica 12 bold')
		label.grid(row=r, column=c)