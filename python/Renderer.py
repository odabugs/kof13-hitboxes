from math import isnan
from ctypes import *
from ctypes.wintypes import *
from directx.d3d import *
from directx.types import *
from directx.d3dx import *

from Global import *
from CStructures import *
from Colors import rgb, changeAlpha, colorByName
import BoxTypes


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

	return user32.DefWindowProcA(c_int(hwnd), c_int(message),
		c_int(wParam), c_int(lParam))


class Renderer:
	def __init__(self, environment, tickerInterval=2):
		self.env = environment
		self.config = self.env.config
		self.process = self.env.process
		self.gameState = self.env.gameState
		self.camera = self.gameState.camera
		self.p1 = self.gameState.p1
		self.p2 = self.gameState.p2
		self.windowsMessage = MSG()

		# TODO: move this BS to config file soon
		self.annotations = argvContains("-annotate")
		self.drawFilling = argvContains("-usefill")
		self.drawBorders = not argvContains("-noborders")
		self.drawPivots  = not argvContains("-nopivots")
		self.syncedMode  = not argvContains("-nosync")
		self.drawTicker  = argvContains("-counter")
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
		self.boxvec = (D3DXVECTOR2 * 5)()
		self.linevec = (D3DXVECTOR2 * 2)()
		
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

		# controls how frequently to check for window movement/resize
		self.updateWindowTickerInterval = tickerInterval
		self.updateWindowTicker = tickerInterval # count down, reset at 0
		
		# frame ticker at the bottom of the screen
		self.frameTicker = 0
		self.frameTickerLimit = 600
		tickerHalfFormat = "%0" + str(digitsIn(self.frameTickerLimit)) + "d"
		self.tickerFormat = tickerHalfFormat + "/" + tickerHalfFormat
		self.tickerWidth = len(self.tickerFormat % (0, 0)) * 10
		self.tickerHeight = 20
		self.tickerTextColor = colorByName("white")
		self.tickerFillColor = changeAlpha(colorByName("black"), 0xB0)
		# set by self.positionTicker()
		self.tickerX = 0
		self.tickerY = 0

		self.boxColors = {1: {}, 2 : {}}
		self.fillBoxColors()
	
	
	def fillBoxColors(self):
		def boxColorsForPlayer(playerID):
			colorsByType = (
				(BoxTypes.BOX_VULNERABLE,  "vulnerable_box_color"),
				(BoxTypes.BOX_COLLISION,   "collision_box_color"),
				(BoxTypes.BOX_ATTACK,      "attack_box_color"),
				(BoxTypes.BOX_THROW,       "throw_box_color"),
				(BoxTypes.BOX_PROJ_VULN,   "projectile_vulnerable_box_color"),
				(BoxTypes.BOX_PROJ_ATTACK, "projectile_attack_box_color"),
				(BoxTypes.BOX_GUARD,       "guard_box_color"),
				(BoxTypes.BOX_PROXIMITY,   "proximity_box_color"),
			)
			lookupColor = lambda option: self.config.get(option, playerID)
			return dict([(p[0], lookupColor(p[1])) for p in colorsByType])

		self.boxColors[1] = boxColorsForPlayer(1)
		self.boxColors[2] = boxColorsForPlayer(2)
	

	def positionTicker(self, onBottom=True):
		yOffset = 15
		self.tickerX = self.centerX - (self.tickerWidth >> 1)
		if onBottom:
			self.tickerY = self.height - self.tickerHeight - yOffset
		else:
			self.tickerY = yOffset


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
		self.process.setKOFRects()
		origin = self.process.kof_origin
		#resolution = self.process.kof_resolution
		br = self.process.kof_bounding_rect
		cr = self.process.kof_client_rect

		self.width = cr.right
		self.height = cr.bottom
		self.centerX = self.width >> 1
		self.centerY = self.height >> 1
		self.scale = self.playerSpriteScale()
		self.baseY = self.baseYOffset()

		self.left,  self.top    = origin.x,  origin.y
		self.right, self.bottom = br.right, br.bottom
		self.positionTicker()


	def hasWindowMoved(self):
		# capture new game window position and size onscreen
		self.process.setKOFRects() # mutates self.process.kof_bounding_rect
		br = self.process.kof_bounding_rect
		origin = self.process.kof_origin
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
				self.process.getLastError())
		
		self.hwnd = user32.CreateWindowExA(
			WS_EX_TOPMOST | WS_EX_COMPOSITED |
			WS_EX_TRANSPARENT | WS_EX_LAYERED, # extended window style
			APP_NAME, # class name for RegisterClassEx
			APP_NAME, # window title
			WS_POPUP, # base window style
			self.process.kof_origin.x, # left X of game window
			self.process.kof_origin.y, # top Y of game window
			self.process.kof_resolution.x, # game window X width
			self.process.kof_resolution.y, # game window Y height
			None, # parent hwnd (none)
			None, # window menu
			hInstance, # instance handle
			None) # "extra" argument

		if not self.hwnd:
			raise Exception("user32.CreateWindowExA: %s" %
				self.process.getLastError())
		
		if oledll.Dwmapi.DwmExtendFrameIntoClientArea(self.hwnd,
		byref(MARGINS(-1, -1, -1, -1))) != S_OK:
			raise Exception("DwmExtendFrameIntoClientArea: %s" %
			self.process.getLastError())

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
			self.spareFillbuf[i].rhw   = 1.0 # don't perform transformations
			self.spareFillbuf[i].color = 0 # clear
		
		memmove(ppVertexBuf2.contents, byref(self.spareFillbuf), vertexBufSize)
		vertexBuf.Unlock()
	

	def createPrimitives(self):
		d3dxdll.D3DXCreateLine(self.device, byref(self.line))
		self.line.SetWidth(1)

		d3dxdll.D3DXCreateFontW(
			self.device,
			24, # font width
			0, # font height
			#400, # font weight
			0, # font weight
			1, # number of mipmap levels
			0, # 1 = italics, 0 = no italics
			0, # character set (0 = ?)
			0, # font rendering precision
			0, # font rendering quality
			0, # font pitch and family index
			LPCWSTR(unicode("fixedsys")), # font typeface
			byref(self.font))
		
		self.createVertexBuffer()
	
	
	def initDirect3D(self):
		self.setDimensions()
		params = D3DPRESENT_PARAMETERS()
		address = d3d.Direct3DCreate9(UINT(D3D_SDK_VERSION))

		if not address:
			raise Exception("Direct3DCreate9: %s" % self.process.getLastError())
		
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
		y = y - (self.lineThickness >> 1) # make pivot align with thick lines
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
			#( 854,  480) : 45,
			( 854,  480) : 49,
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
	def relativeCoords(self, sourceX, sourceY):
		cam = self.camera
		shakeX = round(cam.XShake * self.scale)
		shakeY = round(cam.YShake * self.scale)

		destX = self.centerX + round(sourceX * self.scale) + shakeX
		destY = self.baseY   - round(sourceY * self.scale) - shakeY
		return (int(destX), int(destY))


	def drawPlayerPivots(self):
		def pivotCoords(player):
			ps = player.playerStruct
			return self.relativeCoords(ps.XPivot, ps.YPivot)

		p1pivot = pivotCoords(self.p1)
		p2pivot = pivotCoords(self.p2)
		playerPivots = (p1pivot, p2pivot)
		for pivot in playerPivots:
			self.drawPivot(pivot[0], pivot[1])


	"""
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
	"""


	def drawPlayerHitboxes(self):
		def drawHitboxList(boxList, color):
			for box in boxList:
				left, bottom, width, height = box
				self.drawBoxRelative(left, bottom, width, height, color)

		def drawHitboxesForPlayer(player):
			playerID = player.ID
			for boxType in BoxTypes.hitboxTypes:
				boxListColor = self.boxColors[playerID][boxType]
				boxList = player.hitboxes[boxType]
				drawHitboxList(boxList, boxListColor)

		drawHitboxesForPlayer(self.p1)
		drawHitboxesForPlayer(self.p2)
	

	def drawFrameTicker(self):
		self.frameTicker += 1
		if self.frameTicker >= self.frameTickerLimit:
			self.frameTicker = 0
		
		self.drawFill(
			self.tickerX, self.tickerY,
			self.tickerX + self.tickerWidth,
			self.tickerY + self.tickerHeight,
			self.tickerFillColor) # black
		tickerText = self.tickerFormat % (
			self.frameTicker, self.frameTickerLimit)
		self.drawText(
			self.tickerX, self.tickerY,
			self.tickerWidth, self.tickerHeight,
			self.tickerTextColor, tickerText)


	def renderFrame(self):
		self.gameState.update() # updates p1, p2, camera implicitly
		# has the game window been moved/resized?
		if self.updateWindowTicker == 0:
			self.updateWindowPosition()
			self.updateWindowTicker = self.updateWindowTickerInterval
		self.beginScene()
		
		# draw some hitboxes oh boy!!!!
		self.drawPlayerHitboxes()
		if self.drawPivots:
			self.drawPlayerPivots()

		# draw frame ticker at bottom of screen
		if self.drawTicker:
			self.drawFrameTicker()

		# finish rendering and commit to screen
		self.endScene()
		if self.updateWindowTicker > 0:
			self.updateWindowTicker -= 1
		if self.syncedMode:
			self.pumpMessages()
	

	def runAsynchronous(self):
		while True:
			self.pumpMessages()
