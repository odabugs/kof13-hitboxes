from ctypes import *
from ctypes.wintypes import *
from time import sleep, clock
from struct import pack, unpack
from pydbg import *
from pydbg.defines import *

from CStructures import *
from Renderer import *

user32 = windll.user32
kernel32 = windll.kernel32


# these addresses contain pointers to the player 1 and
# player 2 structs respectively
P1_PTR = 0x008320A0
P2_PTR = 0x008320A4

# camera structure (always seems to be initialized at this address?)
CAMERA_PTR = 0x0082F890
# X and Y offsets used for player sprites when the camera shakes
PLAYER_X_SHAKE = CAMERA_PTR + 0x13C
PLAYER_Y_SHAKE = CAMERA_PTR + 0x140

INT_3 = 0xCC # int 3 opcode in x86 assembly


class HitboxViewer:
	def __init__(self, environment):
		self.env = environment
		self.dbg = self.env.dbg
		self.hooks = self.env.hooks

		self.kof_window = 0 # window ID for main KOF window
		self.kof_pid = 0 # KOF process ID
		self.kof_proc = None # KOF process object
		self.kof_threads = [] # full list of thread IDs used by game
		self.kof_client_rect = None
		self.kof_bounding_rect = None
		self.kof_resolution = None
		self.kof_origin = None

		self.camera = GAME_CAMERA()

		self.p1 = PLAYER()
		self.p2 = PLAYER()
		self.p1_address = 0
		self.p2_address = 0

		self.time = 0
		self.ticks = 0
		self.active = False

		self.breakpoints = {}
	

	def release(self):
		print "Releasing HitboxViewer"
		pass
		print "Released HitboxViewer"
	

	def findGame(self):
		self.bumpProcessPriority()
		self.setKOFWindowID()
		self.setKOFProcessID()
		self.findGameThreads()
		self.setKOFRects()

		self.p1_address = self.readUnsignedDword(P1_PTR)
		self.p2_address = self.readUnsignedDword(P2_PTR)
	
	
	def findGameThreads(self):
		if self.kof_pid == 0:
			return False

		threadEntry = THREADENTRY32()
		threads = []
		TH32CS_SNAPTHREAD = 0x04
		snapshot = kernel32.CreateToolhelp32Snapshot(
				TH32CS_SNAPTHREAD, self.kof_pid)

		if snapshot is None:
			return False

		threadEntry.dwSize = sizeof(threadEntry)
		success = kernel32.Thread32First(snapshot, byref(threadEntry))

		while success:
			if threadEntry.th32OwnerProcessID == self.kof_pid:
				threads.append(threadEntry.th32ThreadID)
			success = kernel32.Thread32Next(snapshot, byref(threadEntry))

		kernel32.CloseHandle(snapshot)
		self.kof_threads = threads
		return threads


	def grabGame(self):
		if not kernel32.DebugActiveProcess(self.kof_pid):
			raise Exception("kernel32.DebugActiveProcess: %s" %
				self.getLastError())
	
	
	def releaseGame(self):
		if not kernel32.DebugActiveProcessStop(self.kof_pid):
			raise Exception("kernel32.DebugActiveProcessStop: %s" %
				self.getLastError())
	

	def setKOFWindowID(self):
		KOF_WINDOW_TITLE = "The King of Fighters XIII"
		interval = 0.05

		while (self.kof_window == 0):
			self.kof_window = user32.FindWindowA(None, KOF_WINDOW_TITLE)
			sleep(interval)
	
	
	def setKOFProcessID(self):
		PROCESS_ALL_ACCESS = 0x001F0FFF
		interval = 0.05
		pid = c_int()
		tid = 0

		while self.kof_pid == 0:
			tid = user32.GetWindowThreadProcessId(self.kof_window, byref(pid))
			self.kof_pid = pid.value
			sleep(interval)

		self.kof_proc = kernel32.OpenProcess(PROCESS_ALL_ACCESS,
		False, self.kof_pid)
	
	
	def setKOFRects(self):
		client_rect = RECT()
		bounding_rect = RECT()
		pt = POINT(0, 0)

		user32.GetClientRect(self.kof_window, byref(client_rect))
		user32.GetWindowRect(self.kof_window, byref(bounding_rect))
		user32.ClientToScreen(self.kof_window, byref(pt))
		
		self.kof_client_rect = client_rect
		self.kof_bounding_rect = bounding_rect
		self.kof_resolution = POINT(client_rect.right, client_rect.bottom)
		self.kof_origin = pt
	

	def bumpProcessPriority(self):
		this_proc = kernel32.GetCurrentProcess()
		kernel32.SetPriorityClass(this_proc, 0x00008000) # above normal
	

	def windowsFormatMessage(self, msg_id):
		def MAKELANGID(primary, sublang):
			return (primary & 0xFF) | (sublang & 0xFF) << 16

		FM_ALLOCATE_BUFFER = 0x0100
		FM_FROM_SYSTEM = 0x1000
		FM_IGNORE_INSERTS = 0x0200
		sys_flag = FM_ALLOCATE_BUFFER | FM_FROM_SYSTEM | FM_IGNORE_INSERTS
		LANG_ENGLISH = 0x09
		SUBLANG_ENGLISH_US = 0x01
		LANG_NEUTRAL = 0x00
		SUBLANG_NEUTRAL = 0x00
		LCID_ENGLISH = MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US)
		LCID_NEUTRAL = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL)
		
		buf = LPWSTR()

		chars = kernel32.FormatMessageW(sys_flag, None, msg_id, LCID_NEUTRAL,
		byref(buf), 0, None)

		if (chars == 0):
			return "No message"

		val = buf.value[:chars]
		kernel32.LocalFree(buf)
		return val


	def getLastError(self):
		return self.windowsFormatMessage(kernel32.GetLastError())


	def _RPM(self, address, buf):
		if not kernel32.ReadProcessMemory(self.kof_proc, address,
		byref(buf), sizeof(buf), None):
			#raise Exception("ReadProcessMemory: %s" % self.getLastError())
			return False
		else:
			return True
	

	def _WPM(self, address, data):
		count = c_ulong(0)
		length = len(data)
		c_data = c_char_p(data[count.value:])
		as_bytes = ", ".join([hex(ord(x))[2:].upper() for x in data])
		print "_WPM: data is [%s]" % as_bytes
		#print "data's type is %s" % type(data)

		if not kernel32.WriteProcessMemory(self.kof_proc, address,
		c_data, length, byref(count)):
			#raise Exception("WriteProcessMemory: %s" % self.getLastError())
			return False
		else:
			print "_WPM: Wrote %i byte(s) at 0x%08X" % (count.value, address)
			return True
	

	def writeWithFormat(self, format_str, address, data):
		return self._WPM(address, pack(format_str, data))
	

	def writeByte(self, address, data):
		return self.writeWithFormat("b", address, data)


	def writeUnsignedByte(self, address, data):
		return self.writeWithFormat("B", address, data)


	def writeWord(self, address, data):
		return self.writeWithFormat("<h", address, data)


	def writeUnsignedWord(self, address, data):
		return self.writeWithFormat("<H", address, data)
	

	def writeDword(self, address, data):
		return self.writeWithFormat("<i", address, data)


	def writeUnsignedDword(self, address, data):
		return self.writeWithFormat("<I", address, data)


	def writeQword(self, address, data):
		return self.writeWithFormat("<q", address, data)


	def writeUnsignedQword(self, address, data):
		return self.writeWithFormat("<Q", address, data)


	def writeFloat(self, address, data):
		return self.writeWithFormat("<f", address, data)

	
	def writeDouble(self, address, data):
		return self.writeWithFormat("<d", address, data)


	def readByte(self, address):
		buffer = c_int8()
		self._RPM(address, buffer)
		return buffer.value


	def readUnsignedByte(self, address):
		buffer = c_uint8()
		self._RPM(address, buffer)
		return buffer.value


	def readWord(self, address):
		buffer = c_int16()
		self._RPM(address, buffer)
		return buffer.value


	def readUnsignedWord(self, address):
		buffer = c_uint16()
		self._RPM(address, buffer)
		return buffer.value


	def readDword(self, address):
		buffer = c_int32()
		self._RPM(address, buffer)
		return buffer.value


	def readUnsignedDword(self, address):
		buffer = c_uint32()
		self._RPM(address, buffer)
		return buffer.value


	def readQword(self, address):
		buffer = c_int64()
		self._RPM(address, buffer)
		return buffer.value


	def readUnsignedQword(self, address):
		buffer = c_uint64()
		self._RPM(address, buffer)
		return buffer.value

	
	def readFloat(self, address):
		buffer = c_float()
		self._RPM(address, buffer)
		return buffer.value


	def readDouble(self, address):
		buffer = c_double()
		self._RPM(address, buffer)
		return buffer.value
	
	
	# set a breakpoint
	def setBP(self, address, handler=None):
		if self.breakpoints.has_key(address):
			print "Address 0x%08X already has a breakpoint set." % address
			return False

		original = self.readUnsignedByte(address)
		self.writeUnsignedByte(address, INT_3)
		self.breakpoints[address] = (hex(address), original, handler)
		return True

	
	def unsetBP(self, address):
		if not self.breakpoints.has_key(address):
			return False
		elif self.readUnsignedByte(address) != INT_3:
			print "No INT 3 opcode found at address 0x%08X" % address
			return False
		
		original = self.breakpoints[address][1]
		self.writeUnsignedByte(address, original)
		del self.breakpoints[address]
		return True


	def eraseBPs(self):
		count = len(self.breakpoints)
		
		for address in self.breakpoints.keys():
			self.unsetBP(address)
		
		print "Removed all %i breakpoints." % count


	def openThread(self, tid):
		THREAD_ALL_ACCESS = 0x001F03FF
		thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, tid)
		return thread


	def getThreadContext(self, tid):
		context = CONTEXT()
		CONTEXT_FULL = 0x00010007
		CONTEXT_DEBUG_REGISTERS = 0x00010010
		context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

		thread = self.openThread(tid)
		if kernel32.GetThreadContext(thread, byref(context)):
			kernel32.CloseHandle(thread)
			return context
		else:
			raise Exception("kernel32.GetThreadContext: %s" %
				self.getLastError())


	def printContext(self, tid, context, display=["general"]):
		def printRegisterSet(regs):
			for reg in regs:
				regName, regValue, regWidth = reg
				formatStr = regName + "\t= 0x%0" + str(regWidth) + "X"
				print formatStr % regValue

		c = context
		generalRegs = (
			("EAX", c.Eax, 8),
			("EBX", c.Ebx, 8),
			("ECX", c.Ecx, 8),
			("EDX", c.Edx, 8),
			("ESI", c.Esi, 8),
			("EDI", c.Edi, 8),
			("ESP", c.Esp, 8),
			("EBP", c.Ebp, 8),
			("EIP", c.Eip, 8),
			("EFLAGS", c.EFlags, 8),
			)
		segmentRegs = (
			("CS", c.SegCs, 4),
			("DS", c.SegDs, 4),
			("ES", c.SegEs, 4),
			("FS", c.SegFs, 4),
			("GS", c.SegGs, 4),
			("SS", c.SegSs, 4),
			)
		debugRegs = (
			("DR0", c.Dr0, 8),
			("DR1", c.Dr1, 8),
			("DR2", c.Dr2, 8),
			("DR3", c.Dr3, 8),
			("DR6", c.Dr6, 8),
			("DR7", c.Dr7, 8),
			)
		allRegs = {
			"general" : generalRegs,
			"segment" : segmentRegs,
			"debug"   : debugRegs
			}
		
		if len(display) == 0:
			print "Name the register set(s) that you want to see " + \
			"by using the \'display\' parameter."
			return

		print "Register values in context on thread 0x%x:" % tid
		for regSet in display:
			printRegisterSet(allRegs[regSet.lower()])

	
	# detect and handle a breakpoint according to its address
	def handleBreakpoint(self, address, tid, context):
		if self.breakpoints.has_key(address):
			handler = self.breakpoints[address][2]
		else:
			handler = None

		result = False
		if handler is not None:
			print "Running handler for breakpoint 0x%x in thread 0x%x" % \
				(address, tid)
			result = handler(address, tid, context)
		else:
			print "Self-handling breakpoint at 0x%x in thread 0x%x" % \
				(address, tid)
			self.printContext(tid, context)
			result = True

		return result

	
	#def handleDebugEvent(self, timeout=0xFFFFFFFF): # INFINITE
	def handleDebugEvent(self, timeout=3000):
		debugEvent = DEBUG_EVENT()
		continueStatus = 0x00010002 # DBG_CONTINUE

		if kernel32.WaitForDebugEvent(byref(debugEvent), timeout):
			self.active = False
			eventCode = debugEvent.dwDebugEventCode
			eventThread = debugEvent.dwThreadId
			#print "Caught debug event %i on thread %s" % \
			#	(eventCode, hex(eventThread))
			
			# is the debug event an exception type?
			EXCEPTION_DEBUG_EVENT = 0x01
			EXCEPTION_BREAKPOINT = 0x80000003

			if eventCode == EXCEPTION_DEBUG_EVENT:
				exception = debugEvent.u.Exception.ExceptionRecord
				exceptionCode = exception.ExceptionCode
				exceptionAddress = exception.ExceptionAddress
				#print "Hit debug event at 0x%x: 0x%x" % \
				#	(exceptionAddress, exceptionCode)

				# did we hit a breakpoint that we set earlier?
				# note: worry about other exception types later
				if exceptionCode == EXCEPTION_BREAKPOINT:
					print "- Hit breakpoint at 0x%x" % exceptionAddress
					threadContext = self.getThreadContext(eventThread)
					result = self.handleBreakpoint(
						exceptionAddress, eventThread, threadContext)
					self.unsetBP(exceptionAddress)

			kernel32.ContinueDebugEvent(
				debugEvent.dwProcessId,
				debugEvent.dwThreadId,
				continueStatus)
		else:
			self.active = False
			raise Exception("kernel32.WaitForDebugEvent: %s" %
				self.getLastError())
	

	def update(self):
		# update camera struct
		self._RPM(CAMERA_PTR, self.camera)

		# update player structs
		self._RPM(self.p1_address, self.p1)
		self._RPM(self.p2_address, self.p2)
