from time import tzname, daylight
from datetime import datetime
import traceback

from pydbg import pydbg
from pydbg.defines import *

from Global import *
from Config import Config
from Renderer import Renderer
from Process import Process
from GameState import GameState

#FRAME_BP = 0x0050EBD0
FRAME_BP = 0x004D6B3F
START_BP = 0x0050DB70

class Main:
	def __init__(self):
		self.dbg = pydbg()
		self.config = Config()
		self.process = Process(self)
		self.gameState = GameState(self)
		self.renderer = Renderer(self)
	

	def runSynchronous(self):
		def renderFrame(dbg):
			self.renderer.renderFrame()
			return DBG_CONTINUE

		def startingHandler(dbg):
			dbg.bp_set(FRAME_BP, handler=renderFrame)
			dbg.bp_del(START_BP)
			return DBG_CONTINUE

		self.process.findGame()
		self.renderer.makeWindow()
		self.renderer.initDirect3D()
		self.dbg.attach(self.process.kof_pid)
		self.dbg.bp_set(START_BP, restore=False, handler=startingHandler)
		self.dbg.run()


	def runAsynchronous(self):
		self.process.findGame()
		self.renderer.makeWindow()
		self.renderer.initDirect3D()
		self.renderer.runAsynchronous()


	def release(self):
		def releaseDebugger():
			# remove all set breakpoints/watchpoints
			#self.dbg.bp_del_all() # why doesn't this work?
			self.dbg.bp_del_hw_all()
			self.dbg.bp_del_mem_all()
			print "Cleaned up pydbg instance"
		
		print "Releasing Main..."
		
		releaseDebugger()
		elements = (
			self.process,
			self.renderer,
		)
		for element in elements:
			if element is not None:
				element.release()
		
		print "Released Main"
	

m = Main()
# for REPL testing
c = m.config
p = m.process
g = m.gameState
p1 = g.p1
p2 = g.p2
r = m.renderer
d = m.dbg


def launch():
	print "Press Ctrl+C in this terminal window at any time to quit."
	try:
		if argvContains("-nosync"):
			m.runAsynchronous() # NOT FOR NORMAL USE
		else:
			m.runSynchronous() # sets a breakpoint ingame
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
