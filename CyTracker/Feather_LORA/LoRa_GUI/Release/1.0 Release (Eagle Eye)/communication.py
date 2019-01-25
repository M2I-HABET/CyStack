#############################################################
#
#	Property of Eagle Eye.
#
#   Authors:
#           Jared Danner
#
#############################################################
import serial.tools.list_ports
import serial
import time
import threading
import globals as g
from tkinter import *
from tkinter.ttk import *


def setup_comms():
	""" Oversees the serial port connection process. """
	print("\nStarting comms setup.----------------------------------")

	# Returns a list of all serial connections.
	ports = get_serial_ports()

	# Validates the current ports to ensure they are Eagle Eye's micro controllers.
	validate_ports(ports)

	# Starets timer based tasks to check for incoming serial data.
	config_scheduler()

	print("Comms setup complete.----------------------------------\n")


def get_serial_ports():
	""" Detects and returns all active serial ports. """

	return list(serial.tools.list_ports.comports())


def validate_ports(ports):
	"""
	Pulls the connected microcontrollers for their name.

	@param ports - Detected serial port connections.
	"""

	print("\nPinging active ports.")

	# COM number.
	com_number = ""
	# Micro-controller descriptor.
	port_description = ""

	# Cycles over all detected ports.
	for port in ports:
		# Temporary serial port variable.
		ser = None
		# If at any point the recreation of the serial port fails. This is set true for debugging.
		passed = True

		# Parses out port info.
		try:
			# Splits the port info.
			com_number, port_description = str(port).split("-")
			# Trims whitespace.
			com_number = com_number.strip()
			# Trims whitespace.
			port_description = port_description.strip()
		# Prints exception handler.
		except Exception as e:
			passed = False
			print("Exception: " + str(e))
			print("Unable to parse: " + str(port))

		# Attempts to recreate serial connection to ensure validity.
		try:
			# If all previous steps have passed, the recreation process coninutes.
			if passed:
				# Creates empty serial object.
				ser = serial.Serial()
				# Assigns the com port number to the serial object.
				ser.port = com_number
				# Assigns the baudrate used in the Eagle Eye project.
				ser.baudrate = 115200
				# Sets the timeout of the serial port to 1 second.
				ser.timeout = 1
				# Opens configured serial port
				ser.open()
		# Prints exception handler.
		except Exception as e:
			passed = False
			print("Exception: " + str(e))
			print("Invalid connection to: " + str(port))

		# Pings microcontroller for name.
		try:
			# If all previous steps have passed, the recreation process coninutes.
			if passed:
				# Debug info.
				print("Pinging: " + port_description)
				# Contacts the Eagle Eye microcontroller to figure out what type of microcontroller its
				# connected to.
				send(ser, "PING")
				# Pauses program execution for 1/10th a second. To allow time for the microcontroller to
				# process the request for info and reply.
				time.sleep(0.1)
				# Reads incoming serial port data from the passed in serial port object.
				response = generic_receive(ser)
				# Checks if microcontroller response matches that of known Eagle Eye hardware.
				if response in "CRAFT_LORA":
					# Creates a serial object instance with the temporary serial object.
					# Class defined at bottom of file.
					PORT_CRAFT_LORA = serial_object(ser, response, port_description)
				elif response in "CRAFT_MEGA":
					# Creates a serial object instance with the temporary serial object.
					# Class defined at bottom of file.
					PORT_CRAFT_MEGA = serial_object(ser, response, port_description)
				elif response in "MC_LORA":
					# Creates a serial object instance with the temporary serial object.
					# Class defined at bottom of file.
					g.PORT_MC_LORA = serial_object(ser, response, port_description)
				# Unknown microcontroller connection.
				else:
					passed = False
					print("Unknown Micro-controller: " + str(response))
		# Prints exception handler.
		except Exception as e:
			passed = False
			print("Exception: " + str(e))
			print("Unknown Response: " + str(response))

		# Prints all info related to port (used for debugging).
		if not passed:
			print("port:" + str(port))
			print("com_number: " + com_number)
			print("port_description: " + port_description)
			print("ser object: " + str(ser))
			print("ser.port: " + ser.port)
			print("ser.baudrate: " + str(ser.baudrate))
			print("port status: " + str(ser.is_open))
		# Otherwise prints the success message of the port.
		else:
			print("Successful setup of: " + str(ser.port))


def config_scheduler():
	"""
	Sets a thread bound timer object to run a method to capture
	serial input every x seconds.
	"""

	try:
		# Checks for valid connection the the mc's Arduino LoRa.
		if g.PORT_MC_LORA is not None:
			print("Scheduling task for mc LoRa.\n")
			g.timer_mc_lora = threading.Timer(0.6, mc_lora_receive)
			g.timer_mc_lora.start()
		# Checks for valid connection the the craft's Arduino MEGA.
		if g.PORT_CRAFT_LORA is not None:
			print("Scheduling task for craft LoRa.\n")
			g.timer_craft_lora = threading.Timer(0.6, craft_lora_receive)
			g.timer.start()
		# Checks for valid connection the the craft's Arduino LoRa.
		if g.PORT_CRAFT_MEGA is not None:
			print("Scheduling task for craft MEGA.\n")
			g.timer_craft_mega = threading.Timer(0.6, craft_mega_receive)
			g.timer_craft_mega.start()
	# Prints exception handler.
	except Exception as e:
		print("Unable to start setup scheduler.")
		print("Exception: " + str(e))


def generic_receive(ser):
	"""
	Responsible for reading in data on the given serial port.
	THIS METHOD RETURNS.

	@param ser - Serial port instance.
	"""

	try:
		# Checks for a incoming data.
		if(ser.in_waiting != 0):
			# Reads in and decodes incoming serial data.
			message = ser.readline().decode()
			# Debug message.
			print("Received from " + str(ser.port) + ". Input: " + message)
			# Return data in string datatype.
			return str(message)
		# No incoming data.
		else:
			return "No response."
	# Prints exception handler.
	except Exception as e:
		print("Exception: " + str(e))
		return "No response."


def mc_lora_receive():
	""" Responsible for reading in data on the given serial port. """

	g.timer_mc_lora = threading.Timer(0.6, mc_lora_receive)
	g.timer_mc_lora.start()
	# Pulls mission_control's serial port object down to a local instanced variable.
	ser = g.PORT_MC_LORA.get_port()
	try:
		# Checks for a incoming data.
		if(ser.in_waiting != 0):
			# Reads in and decodes incoming serial data.
			message = ser.readline().decode()
			# Debug info.
			print("Received from " + str(ser.port) + ". Input: " + message + "\n")
			# Return data.
			g.PORT_MC_LORA.set_input(str(message))
		return
	# Prints exception handler.
	except Exception as e:
		g.timer_mc_lora.cancel()
		print("Exception: " + str(e))
		g.PORT_MC_LORA.set_input("Serial Error")
		return


def craft_lora_receive():
	""" Responsible for reading in data on the given serial port. """

	g.timer_craft_lora = threading.Timer(0.6, mc_lora_receive)
	g.timer_craft_lora.start()
	# Pulls the serial data from the craft LoRa port object down to a local instanced variable.
	ser = g.PORT_CRAFT_LORA.get_port()
	try:
		# Checks for a incoming data.
		if(ser.in_waiting != 0):
			# Reads in and decodes incoming serial data.
			message = ser.readline().decode()
			# Debug info.
			print("Received from " + str(ser.port) + ". Input: " + message + "\n")
			# Return data.
			g.PORT_CRAFT_LORA.set_input(str(message))
		return
	# Print exception handler.
	except Exception as e:
		g.timer_craft_lora.cancel()
		print("Exception: " + str(e))
		g.PORT_CRAFT_LORA.set_input("Serial Error")
		return


def craft_mega_receive():
	""" Responsible for reading in data on the given serial port. """

	g.timer_craft_mega = threading.Timer(0.6, mc_lora_receive)
	g.timer_craft_mega.start()
	# Pulls the serial data from the craft MEGA port object down to a local instanced variable.
	ser = g.PORT_MEGA_LORA.get_port()
	try:
		# Checks for a incoming data.
		if(ser.in_waiting != 0):
			# Reads in and decodes incoming serial data.
			message = ser.readline().decode()
			# Debug info.
			print("Received from " + str(ser.port) + ". Input: " + message + "\n")
			# Return data.
			g.PORT_MEGA_LORA.set_input(str(message))
		return
	# Print exception handler.
	except Exception as e:
		g.timer_craft_mega.cancel()
		print("Exception: " + str(e))
		g.PORT_MEGA_LORA.set_input("Serial Error")
		return


def send(ser, message):
	"""
	Sends passed in parameter over the bound serial port.

	@param ser     - Developer specificed serial port.
	@param message - Paramter to be encoded and sent.
	"""

	# Ensure string datatype.
	message = str(message)
	# Debug info.
	print("Sent to " + str(ser.port) + ". Message: " + message)
	# Checks if port is closed.
	if ser.is_open == False:
		# If true, opens the port.
		ser.open()
	# Encode message to bits & send via serial.
	ser.write(message.encode())


class serial_object():

	def __init__(self, ser, name, description):
		self.ser = ser
		self.port_name = name
		self.context = description
		self.input = StringVar()
		self.input.trace("w", g.mc_class_reference.callback_update_gui)

	def get_context(self):
		"""
		Returns context info.

		@param self - Instance of the class.
		"""

		return self.context

	def get_port_name(self):
		"""
		Returns port ID.

		@param self - Instance of the class.
		"""

		return self.port_name

	def get_port(self):
		"""
		Returns port object.

		@param self - Instance of the class.
		"""

		return self.ser

	def set_input(self, new_input):
		"""
		Sets class input.

		@param self      - Instance of the class.
		@param new_input - Brand new serial port data.
		"""

		self.input.set(new_input)
