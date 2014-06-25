from time import tzname, daylight
from datetime import datetime
import traceback

from pydbg import pydbg
from pydbg.defines import *
import utils

from Global import *
from Renderer import Renderer
from HitboxViewer import HitboxViewer

#FRAME_BP = 0x0050EBD0
FRAME_BP = 0x004D6B3F
START_BP = 0x0050DB70

class Main:
	def __init__(self):
		self.dbg = pydbg()
		self.hooks = utils.hook_container()
		self.viewer = HitboxViewer(self)
		self.renderer = Renderer(self)
	

	def runSynchronous(self):
		def renderFrame(dbg):
			self.renderer.renderFrame()
			return DBG_CONTINUE

		def startingHandler(dbg):
			dbg.bp_set(FRAME_BP, handler=renderFrame)
			stub = lambda dbg: DBG_CONTINUE # "dummy" HW breakpoint handler
			dbg.set_callback(EXCEPTION_BREAKPOINT, stub)
			return DBG_CONTINUE

		self.viewer.findGame()
		self.renderer.makeWindow()
		self.renderer.initDirect3D()
		self.dbg.attach(self.viewer.kof_pid)
		self.dbg.bp_set(START_BP, restore=False, handler=startingHandler)
		self.dbg.run()


	def runAsynchronous(self):
		self.viewer.findGame()
		self.renderer.makeWindow()
		self.renderer.initDirect3D()
		#self.renderer.pumpMessages()
		self.renderer.runAsynchronous()


	def release(self):
		def releaseDebugger():
			# remove all set breakpoints/watchpoints
			#self.dbg.bp_del_all()
			self.dbg.bp_del_hw_all()
			self.dbg.bp_del_mem_all()
			print "Cleaned up pydbg instance"
		
		print "Releasing Main..."
		
		for element in [self.viewer, self.renderer]:
			if element is not None:
				element.release()

		releaseDebugger()
		
		print "Released Main"
	
	
m = Main()
v = m.viewer
r = m.renderer
d = m.dbg
h = m.hooks


def launch():
	print "Press Ctrl+C in this terminal window at any time to quit."
	try:
		if argvContains("-nosync"):
			m.runAsynchronous() # run in asynchronous mode (NOT FOR NORMAL USE)
		else:
			m.runSynchronous() # run in synchronous mode (sets a breakpoint ingame)
	except:
		print "Hit exception in main loop"
		traceback.print_exc()
	finally:
		print "Quitting main loop"
		m.release()


def notice():
	now = datetime.now()
	today = now.strftime("%B %d, %Y at %I:%M %p ") + tzname[daylight]
	contact = "pdk; pdk.odabugs@gmail.com or at forums.shoryuken.com"
	notice = "Please note:\n"
	notice += "This hitbox viewer is currently incomplete and in development."
	notice += "\nThe version shown in this video requires Windows Aero to be"
	notice += "\nenabled in order to work (start KOF XIII with -a in cmdline)."
	notice += "\nCurrently tested only in 1280x720 windowed mode."
	notice += "\nHitbox viewer developed by " + contact
	notice += "\nThis video was recorded on " + today

	print notice

if __name__ == "__main__":
	if argvContains("-notice"):
		notice()
	launch()
