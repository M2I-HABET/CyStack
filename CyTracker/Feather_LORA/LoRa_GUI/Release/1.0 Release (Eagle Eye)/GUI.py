#############################################################
#
#	Property of Eagle Eye.
#
#   Authors:
#           Jared Danner
#
#############################################################
from login_functions import *
from gui_functions import *
from communication import *

LOGIN_ENABLE = False
SERIAL_SELECTED = None


def main():
	"""  Main method of GUI. """

	# Checks for login method.
	if LOGIN_ENABLE:
		# Launches the login terminal.
		login()
		# Launches the main GUI terminal.
		GUI()
	else:
		# Launches the main GUI terminal.
		GUI()


def login():
	"""  Login Screen Config and Generation """

	# Creation of class.
	login = Login_Terminal()
	# Sets the password.
	login.set_credentials("test")
	# Configures and displays the login window.
	login.configure_login_window()


def GUI():
	"""
	Main terminal application for interfacing
	with the Ealge Eye craft.
	"""
	# Creation of class.
	gui = GUI_Terminal()
	# Configures and displays the application window.
	gui.configure_gui_terminal()


# Forces script to start at the method main().
if __name__ == "__main__":
   main()
