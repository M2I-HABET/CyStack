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
import maps as maps
import time
import threading
import globals as g


class MC_Tab():

	def __init__(self, mc_frame):
		"""
		Initialization function for the class.
		@param self     - Instance of the class.
		@param mc_frame - Where this class will place its widgets.
		"""

		# Parent variables.
		self.mc_frame = mc_frame

		# Network variables.
		self.node_mission_control = None
		self.node_payload = None
		self.node_recovery = None
		self.node_platform = None
		self.release_status = None
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

		# Mission Control variables.
		self.mission_control_time = None
		self.payload_time_previous = ""
		self.recovery_time_previous = ""

		# Recovery variables.
		self.recovery_time = None
		self.recovery_latitude = None
		self.recovery_longitude = None


	def variable_setup(self):
		"""
		Initializes classe variables to proper types and starting values.
		@param self - Instance of the class.
		"""

		# StringVar variables are strings that update their text in entries when
		# their value is changed.
		self.mission_control_time = StringVar(self.mc_frame)
		self.recovery_time = StringVar(self.mc_frame)
		self.recovery_latitude = StringVar(self.mc_frame)
		self.recovery_longitude = StringVar(self.mc_frame)
		self.node_mission_control = StringVar(self.mc_frame)
		self.node_payload = StringVar(self.mc_frame)
		self.node_recovery = StringVar(self.mc_frame)
		self.node_platform = StringVar(self.mc_frame)
		self.release_status = StringVar(self.mc_frame)
		self.radio_received = StringVar(self.mc_frame)
		self.radio_sent = StringVar(self.mc_frame)
		self.radio_payload_rssi = StringVar(self.mc_frame)
		self.radio_recovery_rssi = StringVar(self.mc_frame)
		self.radio_payload_last_contact = StringVar(self.mc_frame)
		self.radio_recovery_last_contact = StringVar(self.mc_frame)
		self.radio_last_received_node = StringVar(self.mc_frame)
		self.radio_received_node_id = StringVar(self.mc_frame)
		self.payload_time = StringVar(self.mc_frame)
		self.payload_altitude = StringVar(self.mc_frame)
		self.payload_latitude = StringVar(self.mc_frame)
		self.payload_longitude = StringVar(self.mc_frame)
		self.payload_event = StringVar(self.mc_frame)
		self.payload_speed = StringVar(self.mc_frame)

		# Configures tracing for all variables. When these variables are written to,
		# the corresponding method will run. (Allows for real time display updating)
		self.node_mission_control.trace("w", self.callback_update_mission_control_node_status)
		self.node_payload.trace("w", self.callback_update_payload_node_status)
		self.node_recovery.trace("w", self.callback_update_recovery_node_status)
		self.node_platform.trace("w", self.callback_update_platform_node_status)
		self.release_status.trace("w", self.callback_update_release_status)

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
		self.entry_radio_received = Entry(self.mc_frame, state="readonly", textvariable=self.radio_received, font='Helvtica 11')
		self.entry_radio_sent = Entry(self.mc_frame, state="readonly", textvariable=self.radio_sent, font='Helvtica 11')
		self.entry_radio_payload_rssi = Entry(self.mc_frame, state="readonly", textvariable=self.radio_payload_rssi, font='Helvtica 11')
		self.entry_radio_recovery_rssi = Entry(self.mc_frame, state="readonly", textvariable=self.radio_recovery_rssi, font='Helvtica 11')
		self.entry_radio_payload_last_contact = Entry(self.mc_frame, state="readonly", textvariable=self.radio_payload_last_contact, font='Helvtica 11')
		self.entry_radio_recovery_last_contact = Entry(self.mc_frame, state="readonly", textvariable=self.radio_recovery_last_contact, font='Helvtica 11')
		self.entry_payload_time = Entry(self.mc_frame, state="readonly", textvariable=self.payload_time, justify='right', font='Helvtica 11')
		self.entry_payload_altitude = Entry(self.mc_frame, state="readonly", textvariable=self.payload_altitude, justify='right', font='Helvtica 11')
		self.entry_payload_latitude = Entry(self.mc_frame, state="readonly", textvariable=self.payload_latitude, justify='right', font='Helvtica 11')
		self.entry_payload_longitude = Entry(self.mc_frame, state="readonly", textvariable=self.payload_longitude, justify='right', font='Helvtica 11')
		self.entry_payload_event = Entry(self.mc_frame, state="readonly", textvariable=self.payload_event, justify='right', font='Helvtica 11')
		self.entry_payload_speed = Entry(self.mc_frame, state="readonly", textvariable=self.payload_speed, justify='right', font='Helvtica 11')
		self.entry_radio_received_node_id = Entry(self.mc_frame, state="readonly", textvariable=self.radio_received_node_id, justify='center', font='Helvtica 11')
		self.entry_mission_control_time = Entry(self.mc_frame, state="readonly", textvariable=self.mission_control_time, justify='right', font='Helvtica 11')
		self.entry_recovery_time = Entry(self.mc_frame, state="readonly", textvariable=self.recovery_time, justify='right', font='Helvtica 11')
		self.entry_recovery_latitude = Entry(self.mc_frame, state="readonly", textvariable=self.recovery_latitude, justify='right', font='Helvtica 11')
		self.entry_recovery_longitude = Entry(self.mc_frame, state="readonly", textvariable=self.recovery_longitude, justify='right', font='Helvtica 11')
		self.entry_radio_last_received_node = Entry(self.mc_frame, state="readonly", justify='center', textvariable=self.radio_last_received_node, font='Helvetica 18 bold')


	def create_button_objects(self):
		"""
		Creates/configures button objects.
		@param self - Instance of the class.
		"""

		# Creates button widgets. (Triggers specified callback method.)
		self.button_platform_launch = Button(self.mc_frame, text="Release\nBalloon", command=self.callback_release_balloon)


	def create_label_objects(self):
		"""
		Creates/configures Label objects.
		@param self - Instance of the class.
		"""

		# These objects are banners that are used to give context to each corresponding section
		# of either buttons, display bars, or other objects on the GUI.
		self.label_mission_control_node = Label(self.mc_frame, text="GROUND STATION", relief='solid', anchor="center")
		self.label_mission_control_node.configure(background='red')
		self.label_payload_node = Label(self.mc_frame, text="PAYLOAD", relief='solid', anchor="center")
		self.label_payload_node.configure(background='red')
		self.label_recovery_node = Label(self.mc_frame,  text="RECOVERY", relief='solid', anchor="center")
		self.label_recovery_node.configure(background='red')
		self.label_platform_node = Label(self.mc_frame,  text="PLATFORM", relief='solid', anchor="center")
		self.label_platform_node.configure(background='red')
		self.label_release_status = Label(self.mc_frame, relief='solid', anchor="center")
		self.label_release_status.configure(background='red', text="Pre-Launch")


	def layout_network(self):
		"""
		Binds the sections of widgets related to the network to the top
		portion of the frame.
		@param self - Instance of the class.
		"""

		# Above divider one. (divider at bottom of method)
		self.button_platform_launch.grid(row=3, column=1, sticky='nse')
		self.label_release_status.grid(row=3, column=2, sticky='nswe')
		self.create_label_east(0, 2, self.mc_frame, "Node Status:")
		self.label_mission_control_node.grid(row=0, column=3, sticky='nswe')
		self.label_payload_node.grid(row=1, column=3, sticky='nswe')
		self.label_recovery_node.grid(row=0, column=4, sticky='nswe')
		self.label_platform_node.grid(row=1, column=4, sticky='nswe')
		self.create_label_east(0, 5, self.mc_frame, "Received:")
		self.entry_radio_received.grid(row=0, column=6, columnspan=13, sticky='we')
		self.create_label_east(1, 5, self.mc_frame, "Sent:")
		self.entry_radio_sent.grid(row=1, column=6, columnspan=13, stick='we')
		self.create_label_east(2, 5, self.mc_frame, "RSSI Payload:")
		self.entry_radio_payload_rssi.grid(row=2, column=6, columnspan=1, stick='we')
		self.create_label_east(2, 7, self.mc_frame, "Last Contact (s):")
		self.entry_radio_payload_last_contact.grid(row=2, column=8, columnspan=1, stick='we')
		self.create_label_east(3, 5, self.mc_frame, "RSSI Recovery:")
		self.entry_radio_recovery_rssi.grid(row=3, column=6, columnspan=1, stick='we')
		self.create_label_east(3, 7, self.mc_frame, "Last Contact (s):")
		self.entry_radio_recovery_last_contact.grid(row=3, column=8, columnspan=1, stick='we')
		self.create_label_center(2, 10, self.mc_frame, "Last Packet Received Was From")
		self.entry_radio_last_received_node.grid(row=3, column=10, rowspan=2, sticky='nsew')

		# Terminal divider. KEEP AT THE BOTTOM OF THIS METHOD.
		# This divider is a golden bar strecthing across the screen to provide
		# distinction between variable sections.
		terminal_divider_one = Label(self.mc_frame, background="#F1BE48")
		terminal_divider_one.grid(row=5, column=0, columnspan=20, sticky='we')


	def layout_nodes(self):
		"""
		Binds the sections of widgets related to the payload to the middle
		portion of the frame.
		@param self - Instance of the class.
		"""

		# PAYLOAD
		self.create_label_center(6, 1, self.mc_frame, "PAYLOAD")
		self.create_label_center(7, 0, self.mc_frame, "Up Time (s): ")
		self.entry_payload_time.grid(row=7, column=1, sticky='we')
		self.create_label_center(8, 0, self.mc_frame, "Altitude (m): ")
		self.entry_payload_altitude.grid(row=8, column=1, sticky='we')
		self.create_label_center(9, 0, self.mc_frame, "Latitude:       ")
		self.entry_payload_latitude.grid(row=9, column=1, sticky='we')
		self.create_label_center(10, 0, self.mc_frame, "Longitude:   ")
		self.entry_payload_longitude.grid(row=10, column=1, sticky='we')
		self.create_label_center(11, 0, self.mc_frame, "Event:            ")
		self.entry_payload_event.grid(row=11, column=1, sticky='we')
		self.create_label_center(12, 0, self.mc_frame, "Speed:            ")
		self.entry_payload_speed.grid(row=12, column=1, sticky='we')
		# RECOVERY
		self.create_label_center(6, 6, self.mc_frame, "RECOVERY")
		self.create_label_center(7, 5, self.mc_frame, "Up Time (s): ")
		self.entry_recovery_time.grid(row=7, column=6, sticky='we')
		self.create_label_center(8, 5, self.mc_frame, "Latitude:       ")
		self.entry_recovery_latitude.grid(row=8, column=6, sticky='we')
		self.create_label_center(9, 5, self.mc_frame, "Longitude:   ")
		self.entry_recovery_longitude.grid(row=9, column=6, sticky='we')
		# MISSION CONTROL
		self.create_label_center(6, 10, self.mc_frame, "MISSION CONTROL")
		self.create_label_center(7, 9, self.mc_frame, "Up Time (s):   ")
		self.entry_mission_control_time.grid(row=7, column=10, sticky='we')


	def layout_mission_status(self):
		"""
		Binds the sections of widgets related to mission_control to the bottom
		portion of the frame.
		@param self - Instance of the class.
		"""

		


	def populate_mc_tab(self):
		"""
		Fills the frame with widgets needed for the mission control interface.
		@param self - Instance of the class.
		"""

		# Initializes class variables.
		self.variable_setup()
		# Creates/configures the tk widgets.
		self.create_entry_objects()
		self.create_button_objects()
		self.create_label_objects()
		# Aligns the widgets to the frame's grid.
		self.layout_network()
		self.layout_nodes()
		self.layout_mission_status()
		# Update class instance stored as global.
		g.mc_class_reference = self


	def callback_update_mission_control_node_status(self, *args):
		"""
		Upon serial data notification that the mc_node's network status has been
		updated, this method will change the color of the visual representation on
		the gui to inform the user.
		Green = Connected.
		Yellow = Was, but lost.
		Red = Not connected / lost.
		@param self - Instance of the class.
		"""

		# Refer to above documentation for what the numbers mean.
		if self.node_mission_control.get() in "0.00":
			self.label_mission_control_node.configure(background='red')
		elif self.node_mission_control.get() in "1.00":
			self.label_mission_control_node.configure(background='green')
		elif self.node_mission_control.get() in "2.00":
			self.label_mission_control_node.configure(background='yellow')


	def callback_update_payload_node_status(self, *args):
		"""
		Upon serial data notification that the payload_node's network status has been
		updated, this method will change the color of the visual representation on
		the gui to inform the user.
		Green = Connected.
		Yellow = Was, but lost.
		Red = Not connected / lost.
		@param self - Instance of the class.
		"""

		# Refer to above documentation for what the numbers mean.
		if self.node_payload.get() in "0.00":
			self.label_payload_node.configure(background='red')
		elif self.node_payload.get() in "1.00":
			self.label_payload_node.configure(background='green')
		elif self.node_payload.get() in "2.00":
			self.label_payload_node.configure(background='yellow')


	def callback_update_recovery_node_status(self, *args):
		"""
		Upon serial data notification that the relay_node's network status has been
		updated, this method will change the color of the visual representation on
		the gui to inform the user.
		Green = Connected.
		Yellow = Was, but lost.
		Red = Not connected / lost.
		@param self - Instance of the class.
		"""

		# Refer to above documentation for what the numbers mean.
		if self.node_recovery.get() in "0.00":
			self.label_recovery_node.configure(background='red')
		elif self.node_recovery.get() in "1.00":
			self.label_recovery_node.configure(background='green')
		elif self.node_recovery.get() in "2.00":
			self.label_recovery_node.configure(background='yellow')


	def callback_update_platform_node_status(self, *args):
		"""
		Upon serial data notification that the platform_node's network status has been
		updated, this method will change the color of the visual representation on
		the gui to inform the user.
		Green = Connected.
		Yellow = Was, but lost.
		Red = Not connected / lost.
		@param self - Instance of the class.
		"""

		# Refer to above documentation for what the numbers mean.
		if self.node_platform.get() in "0.00":
			self.label_platform_node.configure(background='red')
		elif self.node_platform.get() in "1.00":
			self.label_platform_node.configure(background='green')
		elif self.node_platform.get() in "2.00":
			self.label_platform_node.configure(background='yellow')


	def callback_update_release_status(self, *args):
		"""
		Upon serial data notification that the release status has been
		updated, this method will change the color of the visual representation on
		the gui to inform the user.
		Green = Connected.
		Yellow = Was, but lost.
		Red = Not connected / lost.
		@param self - Instance of the class.
		"""

		# Refer to above documentation for what the numbers mean.
		if self.release_status.get() in "0.00":
			self.label_release_status.configure(background='red', text="Pre-Launch")
		elif self.release_status.get() in "1.00":
			self.label_release_status.configure(background='yellow', text="Standby..")
		elif self.release_status.get() in "2.00":
			self.label_release_status.configure(background='green', text="Released\nConfirmed")


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
			self.node_mission_control.set("1")
			if(temp_input.count("/") is 5):
				# Splits the received serial data into two respective parts.
				junk, local_vars, radio_in, radio_out, received_rssi, junk = str(temp_input).split("/")
				self.parse_mission_control(local_vars)
				self.parse_payload(radio_in, received_rssi)
				self.parse_recovery(radio_in, received_rssi)
				self.radio_sent.set(radio_out)
				self.radio_received.set(radio_in)
				# Prints input.
				print("---------------------------------------------------------------------------------------------")
				print("Input: " + str(temp_input))
				print("Local: " + str(local_vars) +"\n")
				print("Pkt Received: " + str(radio_in) +"\n")
				print("Pkt Sent: " + str(radio_out) +"\n")
				print("RSSI: " + str(received_rssi) +"\n")
				# SD Card.
				self.log_file = open('mc_data.txt','a') 
				self.log_file.write("---------------------------------------------------------------------------------------------" +"\n")
				self.log_file.write("Input: " + str(temp_input) +"\n")
				self.log_file.write("Local: " + str(local_vars) +"\n")
				self.log_file.write("Pkt Received: " + str(radio_in) +"\n")
				self.log_file.write("Pkt Sent: " + str(radio_out) +"\n")
				self.log_file.write("RSSI: " + str(received_rssi) +"\n")
				self.log_file.close()


	def parse_mission_control(self, local_vars):
		"""
		Parses out variables from given string section.
		Assigns to correct variables.
		
		@param self - Instance of the class.
		@param local_vars - Variables associated with the connected microcontroller.
		"""
		
		# Parses out the mission control timestamp.
		mc_ts = local_vars
		# Sets parsed values to their corresponding StringVar.
		self.mission_control_time.set(mc_ts)


	def parse_payload(self, radio_in, rssi):
		"""
		Parses out variables from given string section.
		Assigns to correct variables.
		
		@param self - Instance of the class.
		@param radio_in - Packet received via radio.
		@param rssi - Relative Signal Strength Index for the received packet.
		"""
		
		# Checksums '$' and non payload variables are thrown out.
		junk, p_ts, p_alt, p_lat, p_lng, p_event, p_speed, junk, junk, junk, junk, node_reset, node_id, junk = str(radio_in).split(",")
		# Sets parsed values to their corresponding StringVar.
		self.payload_time.set(p_ts)
		self.payload_altitude.set(p_alt)
		t_lat = (float(p_lat) / 10000)
		t_lng = (float(p_lng) / 10000)
		self.payload_latitude.set(str(t_lat))
		self.payload_longitude.set(str(t_lng))
		self.payload_event.set(p_event)
		self.payload_speed.set(p_speed)
		self.radio_received_node_id.set(str(node_id))
		# Checks if the packet is from the payload.
		print(self.radio_received_node_id.get())
		# Checks if the packet was from payload.
		if self.radio_received_node_id.get().count("2") is 1:
			# Say you don't receive the a packet in a while. The mission control
			# LoRa still sends you its last known packet each time it tries to
			# update the gui (roughly 1.5 seconds). To prevent the gui from thinking
			# each "gui update" is brand new information, we compare a previous
			# variable value to the proclaimed to be new value. If they are the same, its most
			# likely the same packet we already saw. If they are different, its 100%
			# new.
			if self.payload_time_previous != str(self.payload_time.get()):
				# Node has not power cycled.
				if node_reset.count("1") is 1:
					self.node_payload.set("2")
				# Node has power cycled.
				else:
					self.node_payload.set("1")
				# Updates the appropriate variables.
				self.payload_time_previous = str(self.payload_time.get())
				# Updates the visual indicatior.
				self.radio_last_received_node.set("Payload")
				self.update_payload_rssi(rssi)
		# Constructs a CSV string to be sent to the rotor.
		telemetry = str(self.payload_latitude.get()) + "," + str(self.payload_longitude.get()) + "," + str(self.payload_altitude.get() + "\n\r")
		# Sends data to rotor so it can compute turning angle.
		send_rotor_telemetry(telemetry)
		# Configure a map image from Google Static Maps API.
		new_map_flag = maps.generate_map(self.payload_latitude.get(), self.payload_longitude.get(), "payload")
		# If a new map was created (new GPS coords), places that image into the GUI.
		# maps.
		if new_map_flag is True:
			# Place map onto GUI.

	def parse_recovery(self, radio_in, rssi):
		"""
		Parses out variables from given string section.
		Assigns to correct variables.
		
		@param self - Instance of the class.
		@param radio_in - Packet received via radio.
		@param rssi - Relative Signal Strength Index for the received packet.
		"""
		
		# Checksums '$' and non recovery variables are thrown out.
		junk, junk, junk, junk, junk, junk, junk, junk, r_ts, r_lat, r_lng, node_reset, node_id, junk = str(radio_in).split(",")
		# Sets parsed values to their corresponding StringVar.
		self.recovery_time.set(r_ts)
		t_lat = (float(r_lat) / 10000)
		t_lng = (float(r_lng) / 10000)
		self.recovery_latitude.set(t_lat)
		self.recovery_longitude.set(t_lng)
		self.radio_received_node_id.set(str(node_id))
		# Checks if the packet is from recovery.
		if self.radio_received_node_id.get().count("3") is 1:
			# Say you don't receive the a packet in a while. The mission control
			# LoRa still sends you its last known packet each time it tries to
			# update the gui (roughly 1.5 seconds). To prevent the gui from thinking
			# each "gui update" is brand new information, we compare a previous
			# variable value to the proclaimed to be new value. If they are the same, its most
			# likely the same packet we already saw. If they are different, its 100%
			# new.
			if self.recovery_time_previous != str(self.recovery_time.get()):
				print(node_reset)
				# Node has not power cycled. (1.00)
				if node_reset.count("1") is 1:
					self.node_recovery.set("2")
				# Node has power cycled. (0.00)
				else:
					self.node_recovery.set("1")
				# Updates the appropriate variables.
				self.recovery_time_previous = str(self.recovery_time.get())
				# Updates the visual indicatior.
				self.radio_last_received_node.set("Recovery")
				self.update_recovery_rssi(rssi)
		# Configure a map image from Google Static Maps API.
		maps.generate_map(self.payload_latitude.get(), self.payload_longitude.get(), "recovery")


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


	def callback_release_balloon(self):
		"""
		Triggered by the press of SEND button next to the display_changed_commands entry.
		@param self		- Instance of the class.
		"""

		try:
			# Checks for non-null connection to mission control's lora microcontroller.
			if g.PORT_MISSION_CONTROL_LORA is not None:
				# Manual creation of a serial packet to send to the mission control microcontroller.
				injection_packet = self.create_injection_packet("L")
				# If non-null, send transmission via serial port.
				send(g.PORT_MISSION_CONTROL_LORA.get_port(), injection_packet)
				self.release_status.set("1")
		# Null connection.
		except Exception as e:
			# Prints general error statement. (Used to tell which method errored out)
			print("Invalid connection to mission control's LoRa.")
			print("Exception: " + str(e))


	def create_injection_packet(self, to_be_sent):
		"""
		Creates a manually specified packet to be sent to the connected LoRa node.
		@param self - Instance of the class.
		@param to_be_sent - Info to be sent to the connected microcontroller.
		"""

		new_packet = ""

		try:
			new_packet += "$"
			new_packet += ","
			new_packet += str(to_be_sent)
			new_packet += ","
			new_packet += "$"
			# Returns new packet.
			return new_packet

		# Prints exception handler.
		except Exception as e:
			# Prints general error statement. (Used to tell which method errored out)
			print("Unable to create packet.")
			print("Exception: " + str(e))


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