#############################################################
#
#	Property of Eagle Eye. 
#
#   Authors:
#           Jared Danner
#
#############################################################

from tkinter import *
from tkinter.ttk import *
from mission_control import *
import globals as g


class GUI_Terminal():

	def __init__(self):
		""" 
		Initialization function for the class.

		@param self - Instance of the class.
		"""

		self.gui_window = None
		self.mc_frame = None
		self.craft_frame = None

	def configure_gui_terminal(self):
		""" 
		Configures the main GUI application window to hold
		the required widgets. Displays upon .mainloop().

		@param self - Instance of the class.
		"""

		self.gui_window = Tk()
		self.gui_window.title("Eagle Eye Serial GUI")
		self.gui_window.configure(background='#666666')
		self.gui_window.attributes('-fullscreen', True)
		self.gui_window.bind("<Escape>", self.callback_quit_gui)
		# Creates and defines the notebook object.
		self.configure_notebook()
		# Creates an instance of the mission control oriented class.
		mc_tab = MC_Tab(self.mc_frame)
		# Class call to populate the mission control frame with its widgets.
		mc_tab.main_mc_tab()
		# Displays window.
		self.gui_window.mainloop()

	def configure_notebook(self):
		"""
		Creates and binds the notebook object inside of the GUI terminal.

		@param self - Instance of the class.
		"""

		# Creates a empty Style guideline object.
		theme = Style()
		# Locks the column of buttons switching between different displays to the
		# north west corner of the GUI.
		theme.configure('TNotebook', tabposition='wn')
		# Spacing configuration for individual tabs.
		theme.configure('TNotebook.Tab', padding=10)
		# Sets the background color of each tab.
		theme.configure('TNotebook', background='gray60')
		# Sets the background color of each window.
		theme.configure('TFrame', background="#4d4d4d")
		# Creates the framework of the GUI with the newly defined theme.
		book = Notebook(self.gui_window)
		# Locks the notebook to the left side of the GUI while filling the remainder
		# of the terminal window.
		book.pack(side=LEFT, fill=BOTH, expand=True)
		# Creates an inner frame. (Tab)
		self.mc_frame = Frame(book)
		# Creates an inner frame. (Tab)
		self.craft_frame = Frame(book)
		# The layout of each frame works as a grid system. The next two lines define how many
		# rows and columsn exist on the frames. These row/column numbers are used to 
		# position buttons and displays around the GUI. Weight of 1 just means no button possess more
		# "importance" than other buttons. Just don't change the weight. 
		self.mc_frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19), weight=1)
		self.mc_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22), weight=1)
		# Adds these frames to the GUI terminal. 
		book.add(self.mc_frame, text="Mission Control")
		book.add(self.craft_frame, text="     Eagle Eye       ")


	def callback_quit_gui(self, *args):
		"""
		Bound to the user pressing the 'ESC' key. Kills all active threads
		and shuts down the gui object. This method ensures the program is shutdown
		correctly and doesn't cause a stall due to the still active threads.

		@param self - Instance of the class.
		"""

		# Checks for the existance of specific timer objects.
		if g.timer_mc_lora is not None:
			g.timer_mc_lora.cancel()
		if g.timer_craft_lora is not None:
			g.timer_craft_lora.cancel()
		if g.timer_craft_mega is not None:
			g.timer_craft_mega.cancel()
		# if g.timer_xbox_controller is not None:
		#	g.timer_xbox_controller.cancel()
		# Shuts down the Tkinter GUI.
		self.gui_window.quit()
