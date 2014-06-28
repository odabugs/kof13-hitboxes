from math import isnan
from ctypes import *
from ctypes.wintypes import *
from directx.d3d import *
from directx.types import *
from directx.d3dx import *

from Global import *
from CStructures import *
from Colors import rgb, changeAlpha, colorByName
from BoxColorizer import fixedColor, attackColorizer, nameByID

user32 = windll.user32
kernel32 = windll.kernel32
d3d = windll.d3d9

S_OK = 0
WM_DESTROY = 2
# our vertexes need only 2D position onscreen and color
D3D_VERTEX_FORMAT = D3DFVF.XYZRHW | D3DFVF.DIFFUSE

WS_EX_TOPMOST     = 0x00000008
WS_EX_COMPOSITED  = 0x02000000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED     = 0x00080000
WS_POPUP          = 0x80000000

DT_TOP = 0x0
DT_LEFT = 0x0
DT_NOCLIP = 0x100
DT_SINGLELINE = 0x20
APP_NAME = "HitboxViewerWindow"

PIVOT_SIZE = 12
WHITE = rgb(255, 255, 255)


def wndProc(hwnd, message, wParam, lParam):
	if message == WM_DESTROY:
		user32.PostQuitMessage(0)
		return 0

	"""
	# experiment with capturing mouse clicks on the overlay window
	# (this only seems to work if WS_EX_LAYERED is turned off)
	WM_LBUTTONDOWN = 0x0201
	if message == WM_LBUTTONDOWN:
		MASK = 0xFFFF
		x, y = lParam & MASK, (lParam & (MASK << 16)) >> 16
		print "OH YES (%d, %d)" % (x, y)
	#"""
	return user32.DefWindowProcA(c_int(hwnd), c_int(message),
		c_int(wParam), c_int(lParam))


class Renderer:
	def __init__(self, environment, tickerInterval=2):
		self.env = environment
		self.viewer = self.env.viewer
		self.camera = self.viewer.camera
		self.p1 = self.viewer.p1
		self.p2 = self.viewer.p2
		self.windowsMessage = MSG()

		self.annotations = argvContains("-annotate")
		self.drawFilling = argvContains("-usefill")
		self.drawBorders = not argvContains("-noborders")
		self.drawPivots  = not argvContains("-nopivots")
		self.syncedMode  = not argvContains("-nosync")
		if argvContains("-thicklines"):
			self.lineThickness = 3
		else:
			self.lineThickness = 1
		# control list used in for loops when drawing thick lines
		# (so we aren't creating new list objects all day)
		self.thicknessRange = range(0, self.lineThickness)
		
		# Direct3D created objects
		self.hwnd = None
		self.wndClass = None
		self.d3d = None
		self.device = POINTER(IDirect3DDevice9)()
		self.line = POINTER(ID3DXLine)()
		self.font = POINTER(ID3DXFont)()
		self.fillbuf = None
		self.spareFillbuf = (CUSTOMVERTEX * 4)()

		# reusable resources for drawing primitives
		self.boxvec = (D3DXVECTOR2 * 5)() #((0,0), (0,0), (0,0), (0,0), (0,0))
		self.linevec = (D3DXVECTOR2 * 2)() #((0,0), (0,0))
		
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0
		self.width = 0
		self.height = 0
		self.centerX = 0
		self.centerY = 0
		self.scale = 1.0 # scale factor applied to box coordinates before draw
		self.baseY = 0 # base position onscreen where Y = 0 (i.e., the ground)

		self.updateWindowTickerInterval = tickerInterval
		self.updateWindowTicker = tickerInterval # count down, reset at 0
		
		# frame ticker at the bottom of the screen
		self.frameCounter = 1
		self.frameCounterLimit = 60

		# buffer structures for reading hitbox data from memory
		boxbuf1, boxbuf2 = HITBOX1(), HITBOX2()
		# structure of p1addresses/p2addresses:
		# (player, pointer, colorizer, buffer object, pointer read offset)
		p1addresses = (
			# vulnerable boxes
			(1, 0x007EAC2C, fixedColor(0x0000FF), boxbuf1, 0),
			# collision box
			(1, 0x007EAC08, fixedColor(0x00FFFF), boxbuf2, 8),
			# attack boxes, projectile boxes, normal throws
			(1, 0x007EAC14, attackColorizer, boxbuf1, 0),
			#(1, 0x007EAC14, fixedColor(0xFF0000), boxbuf1, 0),
			# armor and guard/block
			(1, 0x007EAC20, fixedColor(0x00FF00), boxbuf1, 0),
			# proximity detection box (e.g., on Kyo hcb+K or running grabs)
			(1, 0x007EAC38, fixedColor(0xC0C0C0), boxbuf2, 8),
			#(1, 0x007EAC38, fixedColor(0xFFFF00), boxbuf2, 8),
		)
		p2addresses = (
			# vulnerable boxes
			(2, 0x007EAC68, fixedColor(0x4040FF), boxbuf1, 0),
			# collision box
			(2, 0x007EAC44, fixedColor(0x40FFFF), boxbuf2, 8),
			# attack boxes, projectile boxes, normal throws
			(2, 0x007EAC50, attackColorizer, boxbuf1, 0),
			#(2, 0x007EAC50, fixedColor(0xFF4040), boxbuf1, 0),
			# armor and guard/block
			(2, 0x007EAC5C, fixedColor(0x40FF40), boxbuf1, 0),
			# proximity detection box (e.g., on Kyo hcb+K or running grabs)
			(2, 0x007EAC74, fixedColor(0xC0C0C0), boxbuf2, 8),
			#(2, 0x007EAC74, fixedColor(0xFFFF40), boxbuf2, 8),
		)

		# TODO: support configurable draw order based on box type
		self.drawAddresses = interleave(p1addresses, p2addresses)

		#UNKNOWN = [ # what do these do??
			#(0x007EABF0, 0x064000), # black - broken
			#(0x007EAC8C, 0xFF00FF), # magenta - ???
			#(0x007EACC8, 0x800080), # purple - ???
			#(0x007EACD4, 0xFF00FF), # magenta - ???
			#(0x007EAC98, 0x808000), # brown - broken
		#]
	

	def release(self):
		print "Releasing Renderer"
		elements = [
			self.fillbuf,
			self.line,
			self.font,
			self.device,
			self.d3d,
		]
		for element in elements:
			if element is not None:
				print "Releasing %s in Renderer" % element
				element.Release()
		print "Released Renderer"

	
	def setDimensions(self):
		self.viewer.setKOFRects()
		origin = self.viewer.kof_origin
		#resolution = self.viewer.kof_resolution
		br = self.viewer.kof_bounding_rect
		cr = self.viewer.kof_client_rect

		self.width = cr.right
		self.height = cr.bottom
		self.centerX = self.width >> 1
		self.centerY = self.height >> 1
		self.scale = self.playerSpriteScale()
		self.baseY = self.baseYOffset()

		self.left,  self.top    = origin.x,  origin.y
		self.right, self.bottom = br.right, br.bottom


	def hasWindowMoved(self):
		# capture new game window position and size onscreen
		self.viewer.setKOFRects() # mutates self.viewer.kof_bounding_rect
		br = self.viewer.kof_bounding_rect
		origin = self.viewer.kof_origin
		newLeft, newTop = origin.x, origin.y
		newRight, newBottom = br.right, br.bottom

		if ((self.left  != newLeft)  or (self.top    != newTop   ) or
			(self.right != newRight) or (self.bottom != newBottom)):
			return True
		else:
			return False


	def updateWindowPosition(self):
		if not self.hasWindowMoved():
			return
		
		self.setDimensions()
		x, y = self.left, self.top
		width, height = self.width, self.height
		#print "New window position/size: " + repr((x, y, width, height))
		user32.MoveWindow(self.hwnd, x, y, width, height, True)


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
	
	
	# initialize FVF vertex buffer used for drawing box fills
	def createVertexBuffer(self):
		vertexBuf = POINTER(IDirect3DVertexBuffer9)()
		#vertexBuf = IDirect3DVertexBuffer9()
		ppVertexBuf = cast(pointer(vertexBuf), POINTER(c_void_p))
		#ppVertexBuf = POINTER(POINTER(IDirect3DVertexBuffer9))(pVertexBuf)
		vertexBufLength = 4
		vertexBufSize = sizeof(CUSTOMVERTEX) * vertexBufLength

		self.device.CreateVertexBuffer(
			vertexBufSize,
			0, # usage
			D3D_VERTEX_FORMAT,
			D3DPOOL.MANAGED, # store buffer in video RAM
			#cast(ppVertexBuf, POINTER(POINTER(c_void))),
			ppVertexBuf.contents,
			None) # pSharedHandle; THIS MUST ALWAYS BE NULL
		self.fillbuf = vertexBuf
		ppVertexBuf2 = pointer(c_void_p()) # void**
		vertexBuf.Lock(0, 0, ppVertexBuf2, 0)
		
		# initialize vertex buffer here
		for i in range(0, vertexBufLength):
			self.spareFillbuf[i].x     = 0.0
			self.spareFillbuf[i].y     = 0.0
			self.spareFillbuf[i].z     = 1.0 # we don't need this
			self.spareFillbuf[i].rhw   = 1.0
			self.spareFillbuf[i].color = 0 # clear
		
		memmove(ppVertexBuf2.contents, byref(self.spareFillbuf), vertexBufSize)
		vertexBuf.Unlock()
	

	def createPrimitives(self):
		d3dxdll.D3DXCreateLine(self.device, byref(self.line))
		self.line.SetWidth(1)

		d3dxdll.D3DXCreateFontW(
			self.device,
			12, # font width
			0, # font height
			400, # font weight
			1, # number of mipmap levels
			0, # 1 = italics, 0 = no italics
			0, # character set (0 = ?)
			0, # font rendering precision
			0, # font rendering quality
			0, # font pitch and family index
			LPCWSTR(unicode("Verdana")), # font typeface
			byref(self.font))
		
		self.createVertexBuffer()
	
	
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
		params.BackBufferFormat = D3DFORMAT.A8R8G8B8 # ARGB, 32bpp
		#params.MultiSampleType = 0 # D3DMULTISAMPLE_NONE; no multisampling
		
		self.d3d = POINTER(IDirect3D9)(address)

		useHardware = True
		vertexProcessing = 0
		if useHardware:
			vertexProcessing = D3DCREATE.HARDWARE_VERTEXPROCESSING
		else:
			vertexProcessing = D3DCREATE.SOFTWARE_VERTEXPROCESSING
		self.d3d.CreateDevice(
			0,
			D3DDEVTYPE.HAL,
			self.hwnd,
			vertexProcessing,
			byref(params),
			byref(self.device))

		# add error checking on all API calls here
		renderStateOptions = (
			(D3DRS.ZENABLE, False),
			(D3DRS.LIGHTING, False),
			(D3DRS.CULLMODE, D3DCULL.NONE),
			(D3DRS.ALPHABLENDENABLE, True),
			(D3DRS.SRCBLEND, D3DBLEND.SRCALPHA),
			(D3DRS.DESTBLEND, D3DBLEND.INVSRCALPHA),
			(D3DRS.BLENDOP, D3DBLENDOP.ADD),
			(D3DRS.SEPARATEALPHABLENDENABLE, True),
			(D3DRS.SRCBLENDALPHA, D3DBLEND.SRCALPHA),
			(D3DRS.DESTBLENDALPHA, D3DBLEND.INVSRCALPHA),
			(D3DRS.BLENDOPALPHA, D3DBLENDOP.MAX),
		)
		textureStageStateOptions = (
			#(), # currently unused
		)

		self.device.SetFVF(D3D_VERTEX_FORMAT)
		for renderState, rsValue in renderStateOptions:
			self.device.SetRenderState(renderState, rsValue)
		for tsState, tssValue in textureStageStateOptions:
			self.device.SetTextureStageState(0, tsState, tssValue)

		self.createPrimitives()


	def pumpMessages(self):
		msg = self.windowsMessage
		WM_QUIT = 0x0012

		while user32.PeekMessageA(byref(msg), self.hwnd, 0, 0, 1) != 0:
			msgWord = msg.message & 0xFFFF
			if msgWord == WM_QUIT:
				print "Exiting Renderer.pumpMessages loop"
				break
			
			user32.TranslateMessage(byref(msg))
			user32.DispatchMessageA(byref(msg))

		if not self.syncedMode:
			self.renderFrame()
	

	def beginScene(self):
		# TODO: add checks for game window being moved around here
		clearColor = 0 # clear
		self.device.Clear(0, None, D3DCLEAR.TARGET, clearColor, 1.0, 0)
		self.device.BeginScene()
	

	def endScene(self):
		self.device.EndScene()	
		self.device.Present(None, None, None, None)


	def drawLine(self, x1, y1, x2, y2, color):
		points = self.linevec
		points[0].x, points[0].y = (x1, y1)
		points[1].x, points[1].y = (x2, y2)
		self.line.Draw(points, len(points), color)
	

	def drawPivot(self, x, y):
		self.line.SetWidth(self.lineThickness)
		y = y - (self.lineThickness >> 1)
		self.drawLine(x - PIVOT_SIZE, y, x + PIVOT_SIZE, y, WHITE)
		self.drawLine(x, y - PIVOT_SIZE, x, y + PIVOT_SIZE, WHITE)
		self.line.SetWidth(1)
	

	# fancy new fill drawing function
	def drawFill(self, left, top, right, bottom, color):
		spare = self.spareFillbuf
		ppVertexBuf = pointer(c_void_p()) # void**
		vertexBufLength = len(spare)
		vertexBufSize = vertexBufLength * sizeof(CUSTOMVERTEX)

		coords = (
			(left, top   ), (right, top   ),
			(left, bottom), (right, bottom))
		for i in range(vertexBufLength):
			newX, newY = coords[i]
			spare[i].x = float(newX)
			spare[i].y = float(newY)
			spare[i].color = color
		
		self.device.SetStreamSource(0, self.fillbuf, 0, sizeof(CUSTOMVERTEX))
		self.fillbuf.Lock(0, 0, ppVertexBuf, 0)
		memmove(ppVertexBuf.contents, byref(spare), vertexBufSize)
		self.fillbuf.Unlock()
		self.device.DrawPrimitive(D3DPT.TRIANGLESTRIP, 0, 2)
		

	def drawBoxBorders(self, left, top, right, bottom, color):
		pointsLength = len(self.boxvec)
		for offset in self.thicknessRange:
			points = self.boxToVector(
				left  + offset, top    + offset,
				right - offset, bottom - offset)
			self.line.Draw(points, pointsLength, color)
	

	def boxToVector(self, left, top, right, bottom):
		points = self.boxvec
		points[0].x, points[0].y = (left,  top   )
		points[1].x, points[1].y = (right, top   )
		points[2].x, points[2].y = (right, bottom)
		points[3].x, points[3].y = (left,  bottom)
		points[4].x, points[4].y = (left,  top   )
		return points


	def drawBoxRelative(self, left, bottom, width, height, color):
		left,  bottom = self.relativeCoords(left,  bottom)
		width, height = width * self.scale, height * self.scale
		right, top    = left + int(width - 1), bottom - int(height - 1)
		points = self.boxToVector(left, top, right, bottom)
		borderColor = changeAlpha(color, 0xFF)
		innerColor = changeAlpha(color, 0x40)
		
		if self.drawFilling:
			self.drawFill(left, top, right, bottom, innerColor)
		if self.drawBorders:
			self.drawBoxBorders(left, top, right, bottom, borderColor)


	def drawText(self, x, y, width, height, color, text):
		r = RECT(int(x), int(y), int(x + width), int(y + height))
		self.font.DrawTextA(
			None, # 
			text, # 
			-1, # 
			POINTER(RECT)(r), # 
			DT_LEFT | DT_NOCLIP | DT_SINGLELINE, # 
			color)
	
	
	# TODO: fill this in for all resolutions up to at least 1920x1080
	def baseYOffset(self):
		yOffsetsByRes = {
			( 640,  360) : 34,
			( 854,  480) : 45,
			( 960,  540) : 50,
			(1024,  576) : 54,
			(1280,  720) : 67,
			(1366,  768) : 71,
			(1600,  900) : 83,
			#(1920, 1080) : ,
			#(2048, 1152) : ,
			#(2560, 1140) : ,
		}
		res = (self.width, self.height)
		return (self.height - yOffsetsByRes.get(res, 0))


	def playerSpriteScale(self, baseline=480.0):
		# 854x480 ingame resolution displays player sprites at about 1:1 scale
		return (float(self.height) / baseline)

	
	# TODO:
	# - ensure that shaking is handled correctly
	# - fix handling of vertical screen scrolling (e.g., Billy dp+K on hit)
	def relativeCoords(self, sourceX, sourceY):
		cam = self.camera
		shakeX = round(cam.XShake * self.scale)
		shakeY = round(cam.YShake * self.scale)

		destX = self.centerX + round(sourceX * self.scale) + shakeX
		destY = self.baseY   - round(sourceY * self.scale) + shakeY
		return (int(destX), int(destY))

	
	def drawPlayerPivots(self):
		pivotCoords = lambda p: self.relativeCoords(p.XPivot, p.YPivot)
		p1pivot = pivotCoords(self.p1)
		p2pivot = pivotCoords(self.p2)
		playerPivots = (p1pivot, p2pivot)
		for pivot in playerPivots:
			self.drawPivot(pivot[0], pivot[1])
	

	def annotateBox(self, left, bottom, right, top, ID, offset, color):
		relLeft,  relBottom = self.relativeCoords(left,  bottom)
		relRight, relTop    = self.relativeCoords(right, top   )

		coordPair = "(%+0.2f, %+0.2f)"
		coordsFormat = coordPair + "-" + coordPair
		coords = coordsFormat % (left, bottom, right, top)
		flagsStr = "0x%02X" % ID
		result = coords + "; " + flagsStr
		textColor = changeAlpha(color, 255)
		xPosition = relLeft # annotation starts flush with box's left side
		yPosition = relBottom + offset # annotation below box
		#yPosition = relTop - offset # annotation above box
		self.drawText(xPosition, yPosition, 500, 500, textColor, result)


	def drawSingleHitbox(self, character, hitbox, colorizer, offset):
		left,  bottom = hitbox.Left,  hitbox.Bottom
		width, height = hitbox.Width, hitbox.Height
		right, top = left + width, bottom + height
		if (width <= 0.0 or height <= 0.0 or
			isnan(left)  or isnan(bottom) or
			isnan(width) or isnan(height)):
			return False # box could not be drawn
		
		ID = hitbox.BoxID
		color = colorizer(character, ID)
		self.drawBoxRelative(left, bottom, width, height, color)
		if self.annotations:
			self.annotateBox(left, bottom, right, top, ID, offset, color)
		return True # box was drawn

	
	def drawHitboxList(self, character, origin, colorizer, boxbuf, readOffset):
		currentBox = boxbuf
		readToBuffer = self.viewer._RPM
		readPointer = self.viewer.readUnsignedDword
		drawBox = lambda textOffset: self.drawSingleHitbox(
			character, currentBox, colorizer, textOffset)
		# the following two lambdas are side effecting on currentBox
		readNextBoxFrom = lambda address: readToBuffer(address, currentBox)
		readNextBox = lambda: readNextBoxFrom(currentBox.Next1 + readOffset)
		
		# start reading linked list of hitboxes, draw first box
		base = readPointer(readPointer(origin)) + readOffset
		readNextBoxFrom(base) # boxes start at (*(*origin))+readOffset
		drawBox(5)

		# read list of successive boxes; stop when we loop back to the first
		passes, limit = 0, readPointer(origin + 4)
		offset = 10 # text displacement so annotations won't overlap as badly
		while passes < limit: # while currentBox.Next1 != base:
			if not (readNextBox() and drawBox(offset)):
				break
			passes += 1
			offset += 8
	

	def renderFrame(self):
		self.viewer.update() # grab latest game state
		# has the game window been moved/resized?
		if self.updateWindowTicker == 0:
			self.updateWindowPosition()
			self.updateWindowTicker = self.updateWindowTickerInterval
		self.beginScene() # start rendering
		
		# draw some hitboxes oh boy!!!!
		for boxDrawingInfo in self.drawAddresses:
			player, address, colorizer, boxbuf, offset = boxDrawingInfo
			if player == 1:
				character = self.viewer.p1_current
			elif player == 2:
				character = self.viewer.p2_current
			self.drawHitboxList(character, address, colorizer, boxbuf, offset)

		# draw player pivot axes
		if self.drawPivots:
			self.drawPlayerPivots()

		# finish rendering and commit to screen
		self.endScene()
		if self.updateWindowTicker > 0:
			self.updateWindowTicker -= 1
		if self.syncedMode:
			self.pumpMessages()

		#print "p1 current char is " + nameByID(self.viewer.p1_current)
		#print "p2 current char is " + nameByID(self.viewer.p2_current)
		#print "p1 team is " + repr(map(nameByID, self.viewer.p1_team))
		#print "p2 team is " + repr(map(nameByID, self.viewer.p2_team))

		"""
		# experiment with checking window focus
		if user32.GetForegroundWindow() == self.viewer.kof_window:
			print "I AM HAPPY"
		else:
			print "I AM DEPRESSED"
		#"""
	

	def runAsynchronous(self):
		while True:
			self.pumpMessages()
