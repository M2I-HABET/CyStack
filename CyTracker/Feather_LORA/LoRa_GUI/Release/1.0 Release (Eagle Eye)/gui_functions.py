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

		theme = Style()
		theme.configure('TNotebook', tabposition='wn')
		theme.configure('TNotebook.Tab', padding=10)
		theme.configure('TNotebook', background='gray60')
		theme.configure('TFrame', background="#4d4d4d")

		book = Notebook(self.gui_window)
		book.pack(side=LEFT, fill=BOTH, expand=True)

		self.mc_frame = Frame(book)
		self.craft_frame = Frame(book)

		self.mc_frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19), weight=1)
		self.mc_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22), weight=1)

		book.add(self.mc_frame, text="Mission Control")
		book.add(self.craft_frame, text="     Eagle Eye       ")


	def callback_quit_gui(self, *args):
		"""
		Bound to the user pressing the 'ESC' key. Kills all active threads
		and shuts down the gui object. This method ensure the program is shut down
		correctly and doesn't cause a stall due to the still active threads.

		@param self - Instance of the class.
		"""

		if g.timer_mc_lora is not None:
			g.timer_mc_lora.cancel()
		if g.timer_craft_lora is not None:
			g.timer_craft_lora.cancel()
		if g.timer_craft_mega is not None:
			g.timer_craft_mega.cancel()
		# if g.timer_xbox_controller is not None:
		#	g.timer_xbox_controller.cancel()

		self.gui_window.quit()
