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
# import os


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

		# Mission Control variables.
		self.mission_control_time = None
		self.payload_time_previous = ""

		# GUI variables.
		self.display_changed_commands = None


	def variable_setup(self):
		"""
		Initializes classe variables to proper types and starting values.

		@param self - Instance of the class.
		"""

		# StringVar variables are strings that update their text in entries when
		# their value is changed.
		self.mission_control_time = StringVar(self.mc_frame)
		self.operational_mode = StringVar(self.mc_frame)
		self.roll_call_status = StringVar(self.mc_frame)
		self.node_mission_control = StringVar(self.mc_frame)
		self.node_payload = StringVar(self.mc_frame)
		self.node_recovery = StringVar(self.mc_frame)
		self.radio_received = StringVar(self.mc_frame)
		self.radio_sent = StringVar(self.mc_frame)
		self.radio_payload_rssi = StringVar(self.mc_frame)
		self.radio_recovery_rssi = StringVar(self.mc_frame)
		self.radio_payload_last_contact = StringVar(self.mc_frame)
		self.radio_recovery_last_contact = StringVar(self.mc_frame)
		self.radio_last_received_node = StringVar(self.mc_frame)
		self.payload_time = StringVar(self.mc_frame)
		self.payload_altitude = StringVar(self.mc_frame)
		self.payload_latitude = StringVar(self.mc_frame)
		self.payload_longitude = StringVar(self.mc_frame)
		self.payload_event = StringVar(self.mc_frame)
		self.radio_received_node_id = StringVar(self.mc_frame)
		self.display_changed_commands = StringVar(self.mc_frame)

		# Configures tracing for all variables. When these variables are written to,
		# the corresponding method will run. (Allows for real time display updating)
		self.node_mission_control.trace("w", self.callback_update_mission_control_node_status)
		self.node_payload.trace("w", self.callback_update_payload_node_status)
		self.node_recovery.trace("w", self.callback_update_recovery_node_status)
		self.operational_mode.trace("w", self.callback_update_transmission)
		self.roll_call_status.trace("w", self.callback_update_transmission)

		# Initialization of varaible values on GUI startup.
		self.roll_call_status.set("NOT STARTED")
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
		self.radio_received_node_id.set("-------")
		self.mission_control_time.set("-------")
		self.display_changed_commands.set("")
		self.operational_mode.set("NOT STARTED")


	def create_entry_objects(self):
		"""
		Creates/configures entry objects.

		@param self - Instance of the class.
		"""

		# Creates entry widgets for each variable. (Text windows to be placed in the GUI)
		self.entry_operational_mode = Entry(self.mc_frame, state="readonly", textvariable=self.operational_mode, justify='center', font='Helvtica 11')
		self.entry_roll_call_status = Entry(self.mc_frame, state="readonly", textvariable=self.roll_call_status, justify='center', font='Helvtica 11')
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
		self.entry_radio_received_node_id = Entry(self.mc_frame, state="readonly", textvariable=self.radio_received_node_id, justify='center', font='Helvtica 11')
		self.entry_mission_control_time = Entry(self.mc_frame, state="readonly", textvariable=self.mission_control_time, justify='right', font='Helvtica 11')
		self.entry_display_changed_commands = Entry(self.mc_frame, state="readonly", justify='right', textvariable=self.display_changed_commands, font='Helvtica 11')
		self.entry_radio_last_received_node = Entry(self.mc_frame, state="readonly", justify='center', textvariable=self.radio_last_received_node, font='Helvetica 18 bold')


	def create_button_objects(self):
		"""
		Creates/configures button objects.

		@param self - Instance of the class.
		"""

		# Creates button widgets. (Triggers specified callback method.)
		self.button_roll_call_start = Button(self.mc_frame, text="RC Start", command=self.callback_roll_call_start)
		self.button_roll_call_stop = Button(self.mc_frame, text="RC Stop", command=self.callback_roll_call_stop)
		self.button_start_network = Button(self.mc_frame, text="Network Start", command=self.callback_network_start)
		self.button_construct_serial_packet = Button(self.mc_frame, text="Send", command=self.callback_construct_serial_packet)


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


	def layout_network(self):
		"""
		Binds the sections of widgets related to the network to the top
		portion of the frame.

		@param self - Instance of the class.
		"""

		# Above divider one. (divider at bottom of method)
		self.create_label_east(0, 0, self.mc_frame, "Network Status:")
		self.entry_operational_mode.grid(row=0, column=1, sticky='w')
		self.create_label_east(1, 0, self.mc_frame, "Roll Call Status:")
		self.entry_roll_call_status.grid(row=1, column=1, sticky='w')
		self.create_label_east(0, 2, self.mc_frame, "Node Status:")
		self.label_mission_control_node.grid(row=0, column=3, sticky='nswe')
		self.label_payload_node.grid(row=1, column=3, sticky='nswe')
		self.label_recovery_node.grid(row=0, column=4, sticky='nswe')
		self.create_label_east(0, 5, self.mc_frame, "Received:")
		self.entry_radio_received.grid(row=0, column=6, columnspan=14, sticky='we')
		self.create_label_east(1, 5, self.mc_frame, "Sent:")
		self.entry_radio_sent.grid(row=1, column=6, columnspan=14, stick='we')
		self.create_label_east(2, 5, self.mc_frame, "RSSI Payload:")
		self.entry_radio_payload_rssi.grid(row=2, column=6, columnspan=1, stick='we')
		self.create_label_east(2, 7, self.mc_frame, "Last Contact (s):")
		self.entry_radio_payload_last_contact.grid(row=2, column=8, columnspan=1, stick='we')
		self.create_label_east(3, 5, self.mc_frame, "RSSI Recovery:")
		self.entry_radio_recovery_rssi.grid(row=3, column=6, columnspan=1, stick='we')
		self.create_label_east(3, 7, self.mc_frame, "Last Contact (s):")
		self.entry_radio_recovery_last_contact.grid(row=3, column=8, columnspan=1, stick='we')
		self.button_roll_call_start.grid(row=3, column=0, rowspan=2, sticky='nes')
		self.button_roll_call_stop.grid(row=3, column=1, rowspan=2, sticky='ns')
		self.button_start_network.grid(row=3, column=2, rowspan=2, sticky='nws')
		self.create_label_center(2, 10, self.mc_frame, "Last Packet Received Was From")
		self.entry_radio_last_received_node.grid(row=3, column=10, rowspan=2, sticky='nsew')

		# Terminal divider. KEEP AT THE BOTTOM OF THIS METHOD.
		# This divider is a golden bar strecthing across the screen to provide
		# distinction between variable sections.
		terminal_divider_one = Label(self.mc_frame, background="#F1BE48")
		terminal_divider_one.grid(row=5, column=0, columnspan=20, sticky='we')


	def layout_payload(self):
		"""
		Binds the sections of widgets related to the payload to the middle
		portion of the frame.

		@param self - Instance of the class.
		"""

		# Above divider. (divider at bottom of method)
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

		# Terminal divider. KEEP AT THE BOTTOM OF THIS METHOD.
		# This divider is a golden bar strecthing across the screen to provide
		# distinction between variable sections.
		terminal_divider_two = Label(self.mc_frame, background="#F1BE48")
		terminal_divider_two.grid(row=13, column=0, columnspan=20, sticky='we')


	def layout_mission_control(self):
		"""
		Binds the sections of widgets related to mission_control to the bottom
		portion of the frame.

		@param self - Instance of the class.
		"""

		# Below final divider.
		self.create_label_center(14, 1, self.mc_frame, "MISSION CONTROL")
		self.create_label_center(15, 0, self.mc_frame, "Up Time (s):   ")
		self.entry_mission_control_time.grid(row=15, column=1, sticky='we')
		self.create_label_east(22, 1, self.mc_frame, "To Be Sent:")
		self.entry_display_changed_commands.grid(row=22, column=2, columnspan=6, sticky='we')
		self.button_construct_serial_packet.grid(row=22, column=8)


	def main_mc_tab(self):
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
		self.layout_payload()
		self.layout_mission_control()
		# Update class instance stored as global.
		g.mc_class_reference = self
		# Configures serial environment.
		setup_comms()
		# Embeds command line into the gui.
		#self.embed_cmd() # Work in progress for another day.


	# def embed_cmd(self):
		"""
		Creates a inner frame object and links it to the os's command line.

		DOES NOT CURRENT WORK.

		@param self - Instance of the class.
		"""

		# Creation of frame to house the command line / terminal.
		# cmd = Frame(self.mc_frame)
		# Assigns the frames position.
		# cmd.grid(row=5, column=6, columnspan=12, rowspan=6, stick='we')
		# Grabs the system id of the command terminal.
		# wid = cmd.winfo_id()
		# Attempts to bind the terminal into the frame.
		# os.system('xterm -into %d -geometry 40x20 -sb &' % wid)


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
			# N signifies the packet being of normal communication type.
			if "N" in temp_input:
				serial_data, radio_data = str(temp_input).split("]")
				# Variables such as '$' and 'N' are thrown out as junk.
				junk, junk, p_ts, p_alt, p_lat, p_lng, p_event, node_id, mc_ts = str(serial_data).split(",")
				radio_in, radio_out, received_rssi, junk = str(radio_data).split("/")
				# Setting individual variables from the parsed packet.
				self.payload_time.set(p_ts)
				self.payload_altitude.set(p_alt)
				t_lat = (float(p_lat) / 10000)
				t_lng = (float(p_lng) / 10000)
				self.payload_latitude.set(str(t_lat))
				self.payload_longitude.set(str(t_lng))
				self.payload_event.set(p_event)
				self.mission_control_time.set(mc_ts)
				self.radio_received.set(radio_in)
				self.radio_sent.set(radio_out)
				# To retrieve the RSSI value of the last received packet, we need to parse out the radio_in
				# variable to see the node id.
				junk, junk, junk, junk, junk, junk, junk, self.radio_received_node_id, junk = str(radio_in).split(",")
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
			# R signifies the packet being of type Roll Call.
			elif "R" in temp_input:
				# Variables such as '$' and 'R' are thrown out as junk.
				junk, junk, t_mission_control_node_status, t_payload_node_status, t_recovery_node_status, junk = str(temp_input).split(",")
				# Setting individual variables from the parsed packet.
				self.node_mission_control.set(t_mission_control_node_status)
				self.node_payload.set(t_payload_node_status)
				self.node_recovery.set(t_recovery_node_status)



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


	def callback_update_transmission(self, *args):
		"""
		Updates the StringVar used to show user changes in the GUI.

		@param self  - Instance of the class.
		@param *args - Any other random system varaible that gets passed in.
		"""

		temp_packet = ""

		try:
			temp_packet += "$"
			temp_packet += ","
			temp_packet += str(self.operational_mode.get())
			temp_packet += ","
			temp_packet += "$"

			# Displays the changed commands that would be sent to the mission control
			# lora if the user were to press send.
			self.display_changed_commands.set(temp_packet)

		# Prints exeception status.
		except Exception as e:
			# Prints general error statement. (Used to tell which method errored out)
			print("Unable to change packet type.")
			# Prints actual error.
			print("Exception: " + str(e))


	def callback_roll_call_start(self):
		"""
		Triggered by the press of "button_roll_call_start".

		@param self - Instance of the class.
		"""

		self.roll_call_status.set("RUNNING")
		self.operational_mode.set("ROLLCALL")


	def callback_roll_call_stop(self):
		"""
		Triggered by the press of "button_roll_call_stop".

		@param self - Instance of the class.
		"""

		self.roll_call_status.set("FINISHED")
		self.operational_mode.set("STANDBY")


	def callback_network_start(self):
		"""
		Triggered by the press of "button_network_start".

		@param self - Instance of the class.
		"""

		self.operational_mode.set("NORMAL")


	def callback_construct_serial_packet(self):
		"""
		Triggered by the press of SEND button next to the display_changed_commands entry.

		@param self		- Instance of the class.
		"""

		try:
			# Checks for non-null connection to mission control's lora microcontroller.
			if g.PORT_MISSION_CONTROL_LORA is not None:
				# Converts substring into each's corresponding integer value.
				converted_transmission = self.convert_serial()
				# If non-null, send transmission via serial port.
				send(g.PORT_MISSION_CONTROL_LORA.get_port(), converted_transmission)
		# Null connection.
		except Exception as e:
			# Prints general error statement. (Used to tell which method errored out)
			print("Invalid connection to mission control's LoRa.")
			print("Exception: " + str(e))


	def convert_serial(self):
		"""
		Responsible for taking the variables to be set via serial to the mission
		control micro controller and converting them to their correct integer value.

		@param self - Instance of the class.
		"""

		new_packet = ""

		try:
			new_packet += "$"
			new_packet += ","
			new_packet += str(self.convert_op_mode())
			new_packet += ","
			new_packet += "$"
			# Returns new packet.
			return new_packet

		# Prints exception handler.
		except Exception as e:
			# Prints general error statement. (Used to tell which method errored out)
			print("Unable to convert commands.")
			print("Exception: " + str(e))


	def convert_op_mode(self):
		"""
		Converts to correct integer value.

		@param self - Instance of the class.
		"""

		if self.operational_mode.get() == "NOT STARTED":
			return "0.00"
		elif self.operational_mode.get() == "ROLLCALL":
			return "1.00"
		elif self.operational_mode.get() == "STANDBY":
			return "2.00"
		elif self.operational_mode.get() == "NORMAL":
			return "3.00"


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