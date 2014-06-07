from math import isnan, floor
from ctypes import *
from ctypes.wintypes import *
from time import sleep, clock
from struct import pack
from directx.d3d import *
from directx.types import *
from directx.d3dx import *

from Global import *
from CStructures import *

user32 = windll.user32
kernel32 = windll.kernel32
d3d = windll.d3d9

D3DRS_ZENABLE  = 7
D3DRS_LIGHTING = 137
D3DRS_CULLMODE = 22

WS_EX_TOPMOST     = 8
WS_EX_COMPOSITED  = 0x02000000
WS_EX_TRANSPARENT = 32
WS_EX_LAYERED     = 0x00080000
WS_POPUP          = 0x80000000

DT_TOP = 0x0
DT_LEFT = 0x0
DT_NOCLIP = 0x100
DT_SINGLELINE = 0x20
APP_NAME = "HitboxViewerWindow"

WHITE = 0xFFFFFFFF


def wndProc(hwnd, message, wParam, lParam):
	WM_DESTROY = 2
	if message == WM_DESTROY:
		user32.PostQuitMessage(0)
		return 0
	else:
		return user32.DefWindowProcA(c_int(hwnd), c_int(message),
			c_int(wParam), c_int(lParam))


class Renderer:
	def __init__(self, environment):
		self.env = environment
		self.viewer = self.env.viewer
		self.p1 = self.viewer.p1
		self.p2 = self.viewer.p2
		self.camera = self.viewer.camera

		self.drawFilling = not argvContains("-nofill")
		self.drawBorders = not argvContains("-noborders")
		self.drawPivots  = not argvContains("-nopivots")
		self.syncedMode  = not argvContains("-nosync")

		self.hwnd = None
		self.wndClass = None
		self.d3d = None
		self.device = None

		self.line = None
		self.font = None

		# reusable resources for drawing primitives/reading hitboxes
		self.boxvec = (D3DXVECTOR2 * 5) ((0,0), (0,0), (0,0), (0,0), (0,0))
		self.linevec = (D3DXVECTOR2 * 2) ((0,0), (0,0))
		self.boxbuf1 = HITBOX1()
		self.boxbuf2 = HITBOX2()
		
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0
		self.width = 0
		self.height = 0
		self.centerX = 0
		self.centerY = 0
		self.scale = 1.0 # scale factor applied to box coordinates before draw
		
		self.chains = [
			#(0x007EABF0, 0x000000), # black - causes problems
			(0x007EAC14, 0xFFFFFF), # white - works (p1 projectiles)
			#(0x007EAC20, 0xC00000), # crimson - Clark hcf+B
			#(0x007EAC2C, 0xFFFF00), # yellow - works (p1 boxes)
			(0x007EAC50, 0x00FF00), # green - works (p2 projectiles)
			#(0x007EAC5C, 0x0000FF), # blue - ???
			#(0x007EAC68, 0xFFB0B0), # pink - works (p2 boxes)
			#(0x007EAC8C, 0xFF00FF), # magenta - ???
			#(0x007EACC8, 0x800080), # purple - ???
			#(0x007EACD4, 0xFF00FF), # magenta - ???
			#(0x007EAC98, 0x808000), # brown - causes problems
			]
		self.chains2 = [
			#(0x007EAC44, 0xFF0000), # red - player 2 pushbox
			#(0x007EAC08, 0x00FFFF), # cyan - player 1 pushbox
			#(0x007EAC74, 0x008000), # dark green - p2 proximity detect
			#(0x007EAC38, 0xFF00FF), # magenta - 
			]
	

	def release(self):
		print "Releasing Renderer"
		elements = [self.line, self.font, self.device, self.d3d]
		for element in elements:
			if element is not None:
				print "Releasing %s in Renderer" % element
				element.Release()
		print "Released Renderer"

	
	def setDimensions(self):
		origin = self.viewer.kof_origin
		resolution = self.viewer.kof_resolution

		self.width = resolution.x
		self.height = resolution.y
		self.centerX = self.width >> 1
		self.centerY = self.height >> 1
		self.scale = self.playerSpriteScale()

		self.left = origin.x
		self.top = origin.y
		self.right = self.left + self.width
		self.bottom = self.top + self.height


	def makeWindow(self):
		hInstance = kernel32.GetModuleHandleA(None)
		wndClass = WNDCLASS()
		wndClass.style = 0
		wndClass.lpfnWndProc = WNDPROC(wndProc)
		wndClass.cbClsExtra = 0
		wndClass.cbWndExtra = 0
		wndClass.hInstance = hInstance
		wndClass.hIcon = user32.LoadIconA(0, 32512) # I LOVE MAGIC NUMBERS
		wndClass.hCursor = user32.LoadCursorA(0, 32512)
		wndClass.hbrBackground = 0
		wndClass.lpszClassName = APP_NAME
		wndClass.lpszMenuName = APP_NAME
		self.wndClass = wndClass # prevent garbage collection

		if not user32.RegisterClassA(byref(wndClass)):
			raise Exception("user32.RegisterClassA: %s" %
				self.viewer.getLastError())
		
		self.hwnd = user32.CreateWindowExA(
			WS_EX_TOPMOST | WS_EX_COMPOSITED |
			WS_EX_TRANSPARENT | WS_EX_LAYERED,
			APP_NAME,
			APP_NAME,
			WS_POPUP,
			self.viewer.kof_origin.x, # left X of game window
			self.viewer.kof_origin.y, # top Y of game window
			self.viewer.kof_resolution.x, # game window X width
			self.viewer.kof_resolution.y, # game window Y height
			None,
			None,
			hInstance,
			None)

		if not self.hwnd:
			raise Exception("user32.CreateWindowExA: %s" %
				self.viewer.getLastError())
		
		S_OK = 0
		if oledll.Dwmapi.DwmExtendFrameIntoClientArea(self.hwnd,
		byref(MARGINS(-1, -1, -1, -1))) != S_OK:
			raise Exception("DwmExtendFrameIntoClientArea: %s" %
			self.viewer.getLastError())

		# aero must be enabled for the overlay to work
		aeroEnabled = c_int()
		oledll.Dwmapi.DwmIsCompositionEnabled(byref(aeroEnabled))
		if aeroEnabled.value == 0:
			err = "Windows Aero must be enabled for this overlay to work."
			err += "\nPlease restart KOF XIII with the -a command line switch."
			raise Exception(err)
		
		user32.ShowWindow(self.hwnd, 1)
		user32.UpdateWindow(self.hwnd)
	
	
	def createPrimitives(self):
		self.line = POINTER(ID3DXLine)()
		d3dxdll.D3DXCreateLine(self.device, byref(self.line))

		self.font = POINTER(ID3DXFont)()
		d3dxdll.D3DXCreateFontW(
			self.device,
			14, # font width
			0, # font height
			400, # font weight
			1, # number of mipmap levels
			0, # 1 = italics, 0 = no italics
			0, # character set (0 = ?)
			0, # font rendering precision
			0, # font rendering quality
			0, # font pitch and family index
			LPCWSTR(unicode("Arial")), # font typeface
			byref(self.font))


	def initDirect3D(self):
		self.setDimensions()
		params = D3DPRESENT_PARAMETERS()
		address = d3d.Direct3DCreate9(UINT(D3D_SDK_VERSION))

		if not address:
			raise Exception("Direct3DCreate9: %s" % self.viewer.getLastError())
		
		params.Windowed = True
		params.SwapEffect = D3DSWAPEFFECT.DISCARD
		params.BackBufferWidth = self.width
		params.BackBufferHeight = self.height
		params.BackBufferFormat = D3DFORMAT.A8R8G8B8
		params.MultiSampleType = 0 # D3DMULTISAMPLE_NONE; no multisampling
		
		self.d3d = POINTER(IDirect3D9)(address)
		self.device = POINTER(IDirect3DDevice9)()

		useHardware = True
		vertexProcessing = 0
		if useHardware:
			vertexProcessing = D3DCREATE.HARDWARE_VERTEXPROCESSING
		else:
			vertexProcessing = D3DCREATE.SOFTWARE_VERTEXPROCESSING
		self.d3d.CreateDevice(0, D3DDEVTYPE.HAL, self.hwnd,
		vertexProcessing, byref(params), byref(self.device))

		# add error checking on all API calls here
		self.device.SetRenderState(D3DRS_ZENABLE, False)
		self.device.SetRenderState(D3DRS_LIGHTING, False)
		self.device.SetRenderState(D3DRS_CULLMODE, D3DCULL.NONE)

		self.createPrimitives()


	def pumpMessages(self):
		quit = False
		msg = MSG()
		isQuitMsg = 0
		WM_QUIT = 18

		while not quit:
			# 0, 0 = no message type filtering
			#isQuitMsg = user32.GetMessageA(pointer(msg), self.hwnd, 0, 0)
			#isQuitMsg = user32.GetMessageA(pointer(msg), None, 0, 0)
			isQuitMsg = user32.PeekMessageA(pointer(msg), self.hwnd, 0, 0, 1)
			
			if (msg.message & 0xFFFF == WM_QUIT):
				quit = True # this is silly
				print "Exiting Renderer.pumpMessages loop"
				break
			
			user32.TranslateMessage(byref(msg))
			#print "Translated message 0x%x" % msg.message
			user32.DispatchMessageA(byref(msg))
			if not self.syncedMode:
				self.renderFrame()
	

	def beginScene(self):
		# TODO: add checks for game window being moved around here
		clearColor = 0 # clear
		self.device.Clear(0, None, D3DCLEAR.TARGET, clearColor, 1, 0)
		self.device.BeginScene()
	

	def endScene(self):
		self.device.EndScene()	
		self.device.Present(None, None, None, None)


	def setDirect3DFn(self):
		def setDirect3D(address):
			self.d3d = POINTER(IDirect3D9)(address)
			print "Renderer.d3d is now %s" % self.d3d
		return setDirect3D
	
	
	def drawLine(self, x1, y1, x2, y2, width, color):
		points = self.linevec
		points[0].x, points[0].y = (x1, y1)
		points[1].x, points[1].y = (x2, y2)
		self.line.SetWidth(width)
		self.line.Draw(points, len(points), color)
	

	def drawPivot(self, x, y):
		WHITE = 0xFFFFFFFF
		PIVOT_SIZE = 24
		self.line.SetWidth(1)
		self.drawLine(x - PIVOT_SIZE, y, x + PIVOT_SIZE, y, 1, WHITE)
		self.drawLine(x, y - PIVOT_SIZE, x, y + PIVOT_SIZE, 1, WHITE)
	

	# crude, but functional
	def drawRect(self, left, top, right, bottom, color):
		points = self.linevec
		points[0].x = left
		points[1].x = right
		self.line.SetWidth(1)

		for row in range(max(top, 0), min(bottom + 1, self.height - 1)):
			points[0].y = row
			points[1].y = row
			self.line.Draw(points, len(points), color)
	

	def boxToVector(self, left, top, right, bottom):
		points = self.boxvec
		points[0].x, points[0].y = (left,  top   )
		points[1].x, points[1].y = (right, top   )
		points[2].x, points[2].y = (right, bottom)
		points[3].x, points[3].y = (left,  bottom)
		points[4].x, points[4].y = (left,  top   )
		return points


	def drawBoxRelative(self, left, top, right, bottom, color):
		relLeft,  relTop    = self.relativeCoords(left,  top)
		relRight, relBottom = self.relativeCoords(right, bottom)
		points = self.boxToVector(relLeft, relTop, relRight, relBottom)
		
		transparentColor = color & 0x00FFFFFF
		borderColor = color | (0xFF << 24)
		innerColor = transparentColor | (0x40 << 24)
		
		if self.drawFilling:
			self.drawRect(relLeft, relTop, relRight, relBottom, innerColor)
		if self.drawBorders:
			self.line.Draw(points, len(points), borderColor)


	def drawText(self, x, y, width, height, color, text):
		r = RECT(int(x), int(y), int(x + width), int(y + height))
		self.font.DrawTextA(
			None, # 
			text, # 
			-1, # 
			POINTER(RECT)(r), # 
			DT_LEFT | DT_NOCLIP | DT_SINGLELINE, # 
			color)
	
	
	def playerSpriteScale(self, baseline=480.0):
		# 854x480 ingame resolution displays player sprites at about 1:1 scale
		return (float(self.height) / baseline)

	
	def relativeCoords(self, sourceX, sourceY):
		# TODO: Auto-calculate yOff for all screen resolutions
		yOff = 67 # base distance from bottom of screen when sourceY = 0
		cam = self.camera
		shakeX = cam.XShake * self.scale
		shakeY = cam.YShake * self.scale

		destX = self.centerX + (floor(sourceX) * self.scale) + shakeX
		destY = self.height - yOff - (floor(sourceY) * self.scale) + shakeY

		return (int(destX), int(destY))

	
	def drawPlayerPivots(self):
		pivotCoords = lambda p: self.relativeCoords(p.XPivot, p.YPivot)
		p1pivot = pivotCoords(self.p1)
		p2pivot = pivotCoords(self.p2)
		playerPivots = (p1pivot, p2pivot)
		for pivot in playerPivots:
			self.drawPivot(pivot[0], pivot[1])
	

	def drawSingleHitbox(self, hitbox, color=WHITE, offset=5):
		def drawBoxAnnotations(left, top, right, bottom, flags, offset):
			relLeft, relBottom = self.relativeCoords(left, bottom)
			coordPair = "(%+0.2f, %+0.2f)"
			coordsFormat = coordPair + "-" + coordPair
			coords = coordsFormat % (left, bottom, right, top)
			flagsStr = "flags=0x%08X" % flags
			result = coords + "; " + flagsStr
			self.drawText(relLeft, relBottom + offset, 500, 500, color, result)
		
		color = color | (0xFF << 24)
		left,  bottom = hitbox.Left,  hitbox.Bottom
		width, height = hitbox.Width, hitbox.Height
		right, top    = left + width, bottom + height
		#print "Coords: (%f, %f, %f, %f)" % (left, top, right, bottom)
		if (width <= 0.0 or height <= 0.0 or
			isnan(left)  or isnan(right)  or
			isnan(top)   or isnan(bottom)):
			return False # box could not be drawn
		
		self.drawBoxRelative(left, top, right, bottom, color)
		drawBoxAnnotations(left, top, right, bottom, hitbox.Flags, offset)
		return True # box was drawn

	
	def drawHitboxList(self, origin, color, boxbuf, readOffset):
		currentBox = boxbuf
		readToBuffer = self.viewer._RPM
		readPointer = self.viewer.readUnsignedDword
		drawBox = lambda o: self.drawSingleHitbox(currentBox, color, o)
		# the following two lambdas are side effecting on currentBox
		readNextBoxFrom = lambda address: readToBuffer(address, currentBox)
		readNextBox = lambda: readNextBoxFrom(currentBox.Next1 + readOffset)
		
		# start reading linked list of hitboxes, draw first box
		base = readPointer(readPointer(origin)) + readOffset
		readNextBoxFrom(base) # boxes start at (*(*origin))+readOffset
		drawBox(5)

		# read list of successive boxes; stop when we loop back to the first
		passes, limit = 0, 20
		offset = 10
		#while currentBox.Next1 != base and passes < limit:
		while currentBox.Next1 != base:
			if not (readNextBox() and drawBox(offset)):
				break
			passes += 1
			offset += 5
	

	def renderFrame(self):
		# grab latest game state
		self.viewer.update()
		
		# start rendering
		self.beginScene()
		
		# render here
		# draw some hitboxes oh boy!!!!
		self.line.SetWidth(1)
		for chain in self.chains:
			self.drawHitboxList(chain[0], chain[1], self.boxbuf1, 0)
		for chain in self.chains2:
			self.drawHitboxList(chain[0], chain[1], self.boxbuf2, 8)

		# draw player pivot axes
		if self.drawPivots:
			self.drawPlayerPivots()

		#self.drawText(50, 240, 500, 500, 0xFF00FF00, "hello")
		
		# finish rendering and commit to screen
		self.endScene()
