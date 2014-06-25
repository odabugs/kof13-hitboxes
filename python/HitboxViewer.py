from ctypes import *
from ctypes.wintypes import *
from struct import pack, unpack
from time import sleep
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
		self.kof_client_rect = RECT()
		self.kof_bounding_rect = RECT()
		self.kof_resolution = POINT(0, 0)
		self.kof_origin = POINT(0, 0)
		self.camera = GAME_CAMERA()

		self.p1 = PLAYER()
		self.p2 = PLAYER()
		self.p1_address = 0
		self.p2_address = 0
	

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


	def setKOFWindowID(self):
		KOF_WINDOW_TITLE = "The King of Fighters XIII"
		interval = 0.25

		while (self.kof_window == 0):
			self.kof_window = user32.FindWindowA(None, KOF_WINDOW_TITLE)
			sleep(interval)
	
	
	def setKOFProcessID(self):
		PROCESS_ALL_ACCESS = 0x001F0FFF
		interval = 0.25
		pid = c_int()
		tid = 0

		while self.kof_pid == 0:
			tid = user32.GetWindowThreadProcessId(self.kof_window, byref(pid))
			self.kof_pid = pid.value
			sleep(interval)

		self.kof_proc = kernel32.OpenProcess(PROCESS_ALL_ACCESS,
		False, self.kof_pid)
	
	
	def setKOFRects(self):
		user32.GetClientRect(self.kof_window, byref(self.kof_client_rect))
		user32.GetWindowRect(self.kof_window, byref(self.kof_bounding_rect))
		self.kof_origin.x = 0
		self.kof_origin.y = 0
		user32.ClientToScreen(self.kof_window, byref(self.kof_origin))
		
		self.kof_resolution.x = self.kof_client_rect.right
		self.kof_resolution.y = self.kof_client_rect.bottom
	
	
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
	
	
	def update(self):
		# update camera struct
		self._RPM(CAMERA_PTR, self.camera)

		# update player structs
		self._RPM(self.p1_address, self.p1)
		self._RPM(self.p2_address, self.p2)
