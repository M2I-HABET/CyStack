#############################################################
#
#	Property of HABET.
#
#   Authors:
#           Jared Danner
#
#############################################################

from tkinter import *
import globals as g

class Login_Terminal():

	def __init__(self):
		"""
		Initialization function for the class.

		@param self - Instance of the class.
		"""

		self.password = ""
		self.login_window = None
		# What the user enters. Will be compared against set password.
		self.entry_credentials = None
		# If the user has given the correct password. Seems redundant,
		# but is used to prevent the user from closing the login
		# window and bypassing the credentials page.
		self.lock_state = True
		# List of acceptable passwords.
		self.mission_control_password = "mc"
		self.recovery_password = "recovery"
		self.admin_password = "admin"
		self.dev_password = "dev"


	def set_credentials(self, password):
		"""
		Sets the developer's desired user and pass.

		@param self     - Instance of the class.
		@param password - Password to be set.
		"""

		self.password = password


	def callback_verify_credentials(self, event=None):
		"""
		Checks user's password versus actual password.
		returns True if match, False otherwise.

		@param self  - Instance of the class.
		@param event - Triggered by press of the enter button.
		"""

		# Grabs the text of entry and compares against password.
		if self.entry_credentials.get() in self.mission_control_password:
			# If match, prints to cmd and destroys TK window.
			print("PASSWORD MATCH")
			# Updates lock state appropriately.
			self.lock_state = False
			# Upon deletion, this class will return to its GUI.py method.
			self.login_window.destroy()
			# Sets up system for admin
			g.SYSTEM_USER = "mc"
		elif self.entry_credentials.get() in self.recovery_password:
			# If match, prints to cmd and destroys TK window.
			print("PASSWORD MATCH")
			# Updates lock state appropriately.
			self.lock_state = False
			# Upon deletion, this class will return to its GUI.py method.
			self.login_window.destroy()
			# Sets up system for admin
			g.SYSTEM_USER = "recovery"
		elif self.entry_credentials.get() in self.admin_password or self.dev_password:
			# If match, prints to cmd and destroys TK window.
			print("PASSWORD MATCH")
			# Updates lock state appropriately.
			self.lock_state = False
			# Upon deletion, this class will return to its GUI.py method.
			self.login_window.destroy()
			# Sets up system for admin
			g.SYSTEM_USER = "admin"
		else:
			# If different. Prints to user and aways for next try.
			print("WRONG PASSWORD")


	def configure_login_window(self):
		"""
		Configures the login window to hold the appropriate
		buttons and entries. Displays upon .mainloop().

		@param self - Instance of the class.
		"""

		# Creates the Tkinter popup window.
		self.login_window = Tk()
		# Sets title.
		self.login_window.title("Verify Credentials")
		# Sets the background color.
		self.login_window.configure(background='gray')
		# Dimensions of future Tkinter window. (Units are in pixels)
		window_width = 500
		window_height = 270
		# Dimensions of current computer monitor.
		screen_width = self.login_window.winfo_screenwidth()
		screen_height = self.login_window.winfo_screenheight()
		# Math to move the generation point to have the TK window be centered.
		x_coord = (screen_width/2) - (window_width/2)
		y_coord = (screen_height/2) - (window_height/2)
		# Configures the point the window will display at.
		self.login_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coord, y_coord))
		# Picture.
		eagle_eye_picture = PhotoImage(file="Eagle Eye Banner.PNG")
		title_picture = Label(self.login_window, image=eagle_eye_picture)
		title_picture.pack()
		# User entry.
		self.entry_credentials = Entry(self.login_window,
								  justify='center',
								  font="Helvetica 20 bold")

		self.entry_credentials.pack(padx=150, pady=30, fill='x')
		# Login button.
		button_login = Button(self.login_window,
							  text='Login',
							  font="Helvetica 10 bold",
							  command=self.callback_verify_credentials)
		button_login.pack()
		# Forces the operating system to adjust top level
		# focus to this application widget.
		self.entry_credentials.focus()
		# Creates a hotkey for the enter button to automate the button press "button_login".
		self.login_window.bind('<Return>',self.callback_verify_credentials)
		# Displays the window and pauses until user interaction.
		self.login_window.mainloop()
