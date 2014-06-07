
"""
This module contains some useful and general
functionality needed in most Direct3D applications.
The Frame class is similar to the one in DirectPython,
altough it is now more complex in order to meet the needs of
lower-level COM-programming.
"""

#*************************************************
#   direct.utl.py
#
#   Extension module for directx for Python.
#
#   TODO: Too much hard-coded "magic" values - make constants.
#
#      Author:  Heikki Salo
#   Copyright:  (c) 2006 by Heikki Salo
#     Created:  3.8.2006
#
#*************************************************

import time
import sys

from directx.types import *
from directx.d3d import IDirect3D9, IDirect3DDevice9, IDirect3DTexture9
from directx.d3dx import d3dxdll, TestHR, ID3DXFont, ID3DXMesh, ID3DXBuffer, D3DXMATERIAL   
    
    
#*************************************************
#   Structures and other definitions. 
#*************************************************
    
__all__ = ["IsMouseMessage", "Frame"]
    
#Window styles
WINDOWED = 0x00C00000 | 0x00080000 | 0x00040000 | 0x00020000 | 0x00010000 
FULLSCREEN = 0x80000000L
    
WNDPROC = WINFUNCTYPE(c_long, HWND, UINT, WPARAM, LPARAM)
    
class WNDCLASS(Structure):
    _fields_ = [
        ('style', c_uint),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', c_int),
        ('cbWndExtra', c_int),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', c_int),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', c_char_p),
        ('lpszClassName', c_char_p)
    ]
    
#*************************************************
#   Misc utility functions.  
#*************************************************
    
def _ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle           
     
def IsMouseMessage(msg):
    """Returns True if the message is a Windows mouse message."""
    return (msg >= 0x0200 and msg <= 0x020D) 
    
def PrintMaterial(material):
    attribs, values = ("Diffuse", "Ambient", "Specular", "Emissive"), ("r", "g", "b", "a")
    for name in attribs:
        a = getattr(material, name)
        for value in values:
            print name + "." + value, getattr(a, value)
        print     
    
#*************************************************
#   The Frame class - an old friend from DirectPython.
#   The interface is similar but most of the guts
#   are totally different.
#*************************************************
    
_framehelp = u"""\
F1: toggle help/show options
F10: toggle fullscreen
F8: toggle wireframe
P: pause
Esc: quit"""

class Frame(object):
    """Basic framework class that handles common tasks
       required from a Direct3D application. Be careful
       with different resources: failing to release
       them in required callback can crash or put
       the Frame into an infinite loop (altough it
       still handles messages and can be closed by
       the user)."""
    _activeframe = None
    
    def __init__(self, title, size=(800, 600)):
        """The constructor initializes attributes and
           creates all basic resources."""
        #Window stuff
        self.hwnd = None
        self.wndclass = None
        
        #DirectX stuff
        self.d3dobject = None
        self.device = None
        self.font = None
        self.presentparams = None
        
        #General info
        self.fullscreen = True
        self.fullscreenres = (1024, 768)
        self.time = 0.0
        self.elapsedtime = 0.0
 
        #Help
        self.help = u"No help"
        self.showhelp = False
        
        #Private stuff.
        self._hooks = []
        self._timers = []
        self._pauses = 0
        self._pausestart = 0.0
        self._pausetime = 0.0  
        self._resizing = False
        self._fillmode = D3DFILL.SOLID
        self._texturecache = {}
        self._meshcache = {}
        #Save the FPU-accuracy.
        #self._fpuword = cdll.msvcr71._control87(UINT(0), UINT(0x00030000))
        
        #Thread
        self._monitorthread = None
        self._monitor = False
        
        #Create the enviroment.
        
        self.CreateWindow(title)
        
        if self._monitor:
            import threading
            self._monitorthread = threading.Thread(target=self.__MonitorThread)
            self._monitorthread.start()
        
        self.ToggleFullscreen()
        self.OnInit()
           
    def __MonitorThread(self):
        while self._monitor:
            #Only for debugging!
            if windll.user32.IsHungAppWindow(self.hwnd):
                print "Frame window not responding, closing the application."
                import os
                os._exit(1)
            time.sleep(0.2)
        
    def LoadMesh(self, name, usecache=True):
        """Loads a mesh and it's materials from the given file. By default
           they are looked up and saved to a cache. This can
           be disabled by setting the second usecache-parameter to False."""
        name = name.strip().lower()
        if usecache:
            try:
                return self._meshcache[name]
            except KeyError:
                pass
        
        mesh = POINTER(ID3DXMesh)()
        materialcount = DWORD()
        materialbuffer = POINTER(ID3DXBuffer)()
        
        d3dxdll.D3DXLoadMeshFromXA.restype = TestHR
        d3dxdll.D3DXLoadMeshFromXA(LPSTR(name),
            D3DXMESH.MANAGED, self.device, None, 
            byref(materialbuffer), None, 
            byref(materialcount), byref(mesh))
        
        #Save the materials to a normal Python list.
        materials = cast(materialbuffer.GetBufferPointer(), POINTER(D3DXMATERIAL))
        resultmaterials = []
        for i in xrange(materialcount.value):
            resultmaterials.append(materials[i].MatD3D)
        
        data = (mesh, resultmaterials)
        if usecache:
            self._meshcache[name] = data
        return data
        
    def LoadTexture(self, name, usecache=True):
        """Loads a texture from the given file. By default
           they are looked up and saved to a cache. This can
           be disabled by setting the second usecache-parameter
           to False."""
        name = name.strip().lower()
        if usecache:
            try:
                return self._texturecache[name]
            except KeyError:
                pass

        texture = POINTER(IDirect3DTexture9)()
        
        d3dxdll.D3DXCreateTextureFromFileExA.restype = TestHR
        d3dxdll.D3DXCreateTextureFromFileExA(self.device, 
            LPSTR(name), 0, 0, 0, 0, D3DFORMAT.UNKNOWN, 
            D3DPOOL.MANAGED, D3DX_DEFAULT, 
            D3DX_DEFAULT, 0, None, None, byref(texture)) 
            
        #Add to cache and return.
        if usecache:
            self._texturecache[name] = texture
        return texture
        
    def ClearCache(self):
        """Clears textures, meshes and similar
           objects from the cache. Mostly called
           internally. """
        self._texturecache.clear() 
        self._meshcache.clear()
        
    def SetMessageHook(self, callback):
        """Set a message hook function which will receive
           all window messages even before they reach the Frame's
           own handlers. The callback should return True if it
           has handled the message in which case the Frame will
           not receive it. The returned values can be used to
           remove the hook when it is no longer needed by passing
           the value to RemoveMessageHook()"""
        self._hooks.append(callback)
        return len(self._hooks) - 1
           
    def RemoveMessageHook(self, index):
        """Removes a message hook."""
        del self._hooks[index]
           
    def SetTimer(self, timeout, callback, args=()):
        """Set a timer function that is called (with args) after the
           given amount of time (in seconds) has elapsed. If the
           callback returns True, the timer is reset and called
           again after the time has passed. The returned value
           can be passed to RemoveTimer() which removes the active
           timer. Alternatively you can just wait the timer to
           expire (callback returns non-True value), in which 
           case it is removed."""
        self._timers.append([self.time, timeout, callback, args])
        return len(self._timers) - 1          
           
    def RemoveTimer(self, index):
        """Removes a timer."""
        del self._timers[index]
           
    def _CheckTimers(self):
        """Check if any timers need to run. Called internally."""
        assert (self._pauses == 0)
        for i, timer in enumerate(self._timers[:]):
            if timer[0] + timer[1] <= self.time:
                #Call the callback.
                if timer[2](*timer[3]):
                    #Renew the timer.
                    timer[0] = self.time
                else:
                    #Remove the timer.
                    del self.timers[i]      
        
    def CreateWindow(self, title):
        """This function should create or use an existing window.
           This method is called only once and it can be overriden. """
        #Call this only once.
        assert (self.hwnd is None)
    
        CreateWindowEx = windll.user32.CreateWindowExA
        CreateWindowEx.argtypes = [c_int, c_char_p, c_char_p, c_int, 
            c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
        CreateWindowEx.restype = _ErrorIfZero

        #Define Window Class
        wndclass = WNDCLASS()
        wndclass.style = 0
        wndclass.lpfnWndProc = WNDPROC(_WndProc)
        wndclass.cbClsExtra = wndclass.cbWndExtra = 0
        wndclass.hInstance = windll.kernel32.GetModuleHandleA(c_int(0))
        wndclass.hIcon = windll.shell32.ExtractIconA(
            wndclass.hInstance, LPCSTR("textures/x.ico"), 0)
        wndclass.hCursor = windll.user32.LoadCursorA(
            HINSTANCE(0), LPSTR(32512)) 
        try:
            wndclass.hbrBackground = windll.gdi32.GetStockObject(INT(4))
        except:
            pass
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = "MainWin"
        
        #Register Window Class
        if not windll.user32.RegisterClassA(byref(wndclass)):
            raise WinError()
            
        self.wndclass = wndclass
        self.hwnd = HWND(CreateWindowEx(0, wndclass.lpszClassName, title,
            WINDOWED, 0, 0, 100, 100, 0, 0, wndclass.hInstance, 0))

    def CreateDevice(self):
        """Creates a new device and cleans any old resources if
           they exist. Usually called only once."""
        #Empty the cache, this might cause the 
        #old device (if any) to die.
        self.ClearCache()
              
        if self.device:
            self.OnLostDevice()
            self.OnDestroyDevice()
            self.font = None
            self.device = None
    
        if not self.d3dobject:
            #First time, create the object.
            address = windll.d3d9.Direct3DCreate9(UINT(D3D_SDK_VERSION))
            self.d3dobject = POINTER(IDirect3D9)(address)
            if self.d3dobject == 0:
                raise RuntimeError(
                    "Can't create IDirect3D9. Make sure that you have DirectX 9.0c installed.")
     
        best = None
        if self.fullscreen:
            #"Best" formats first.
            formats = (D3DFORMAT.A8R8G8B8, D3DFORMAT.X8R8G8B8)
            
            for format in formats:
                for i in xrange(self.d3dobject.GetAdapterModeCount(0, format)):
                    mode = D3DDISPLAYMODE()
                    try:
                        self.d3dobject.EnumAdapterModes(0, 
                            format, i, byref(mode))
                    except:
                        #No support.
                        continue
                        
                    if mode.Width != self.fullscreenres[0] or mode.Height != self.fullscreenres[1]:
                        #Wrong size.
                        continue
                    
                    if best is None:
                        #First hit
                        best = mode

                    if mode.RefreshRate > best.RefreshRate:
                        #Better refreshrate.
                        best = mode  
        else:
            #Windowed mode
            best = D3DDISPLAYMODE(0, 0, 0, D3DFORMAT.UNKNOWN)
          
        assert (best is not None) #No valid mode found
          
        params = D3DPRESENT_PARAMETERS()
        params.BackBufferWidth = best.Width
        params.BackBufferHeight = best.Height
        params.BackBufferFormat = best.Format
        params.BackBufferCount = 1
        params.MultiSampleType = 0
        params.MultiSampleQuality = 0
        params.SwapEffect = D3DSWAPEFFECT.DISCARD
        params.hDeviceWindow = self.hwnd
        params.Windowed = not self.fullscreen
        params.EnableAutoDepthStencil = True
        params.AutoDepthStencilFormat = D3DFORMAT.D16
        params.Flags = 0
        params.FullScreen_RefreshRateInHz = best.RefreshRate
        params.PresentationInterval = D3DPRESENT.INTERVAL_ONE
    
        #Create a device.
        self.device = POINTER(IDirect3DDevice9)()
        self.d3dobject.CreateDevice(0, D3DDEVTYPE.HAL, self.hwnd, 
            D3DCREATE.HARDWARE_VERTEXPROCESSING | D3DCREATE.NOWINDOWCHANGES | 
            D3DCREATE.FPU_PRESERVE, byref(params), byref(self.device))
    
        self.presentparams = params
    
        #Create a font.
        self.font = POINTER(ID3DXFont)()
        d3dxdll.D3DXCreateFontW.restype = TestHR
        d3dxdll.D3DXCreateFontW(self.device, INT(-14), UINT(0), UINT(700),
            UINT(0), BOOL(0), DWORD(0), DWORD(0), DWORD(0), DWORD(0), 
            LPCWSTR(u"Arial"), byref(self.font))
    
        self.OnCreateDevice()
        self.OnResetDevice()
    
    def Mainloop(self):
        """Starts the mainloop. The loop will call
        callbacks and handle messages. """
        Frame._activeframe = self
        
        self.time = time.clock()
        
        while 1:
            #We run this loop as fast as possible. 
            #Add some throttling if needed.
            if not self._pauses:
                self.OnUpdate()
        
            self.device.Clear(0, None, D3DCLEAR.TARGET | D3DCLEAR.ZBUFFER, 
                0xff0000ff, 1.0, 0)
            self.device.BeginScene()
            self.device.SetRenderState(D3DRS.FILLMODE, self._fillmode)
            
            self.OnRender()
            
            #The help string. 
            text = _framehelp
            if self.showhelp: 
                text = self.help

            textarea = RECT(10, 10, self.presentparams.BackBufferWidth - 10, 
                self.presentparams.BackBufferHeight - 10)
            self.font.DrawTextW(None, text, -1, textarea, 
                D3DXFONT.LEFT | D3DXFONT.TOP | D3DXFONT.WORDBREAK, 
                0xffffff00)

            self.device.EndScene()
            try:
                self.device.Present(None, None, 0, None) 
            except:
                self.ResetDevice()
    
            if self._pauses:
                #Paused, time does not advance.
                self.elapsedtime = 0.0
            else:
                #Go go go.
                newtime = time.clock() - self._pausetime
                self.elapsedtime = newtime - self.time 
                self.time = newtime
                
                self._CheckTimers()
                
            self.ProcessMessages()
           
        self.Quit()   
           
    def Quit(self, status=0):
        """Ends the Mainloop() and possibly the
           whole application. The status will
           be passed to sys.exit(). Call this if
           you want to exit, this also performs
           some important cleanup. """
        self.OnClose()
        self.OnDestroyDevice()

        Frame._activeframe = None
    
        del self.font
        del self.device
        del self.d3dobject
    
        if self._monitorthread:
            self._monitor = False
            self._monitorthread.join()
    
        if self.wndclass:
            #We created the window (maybe). CreateWindow can
            #be overriden to use some other window.
            if self.wndclass.hIcon:
                windll.user32.DestroyIcon(self.wndclass.hIcon)
        
            if windll.user32.IsWindow(self.hwnd):
                #Still alive (= we are not quitting because
                #of WM_QUIT) - destroy the window.
                windll.user32.DestroyWindow(self.hwnd)
        
            windll.user32.UnregisterClassA(
                self.wndclass.lpszClassName, 
                self.wndclass.hInstance)        
              
        #Exit (maybe) via exception.
        sys.exit(int(status))
    
    def ProcessMessages(self):
        """Process all waiting messages."""
        msg = MSG()
        msgptr = pointer(msg)
        NULL = HWND(0)
        while windll.user32.PeekMessageA(msgptr, NULL, UINT(0), UINT(0), UINT(0x0001)) != 0:
            windll.user32.TranslateMessage(msgptr)
            windll.user32.DispatchMessageA(msgptr)
            if msg.message == 0x0012: #WM_QUIT
                self.Quit(msg.wParam)
    
    def SetTransform(self, trans=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
        """Same as in DirectPython."""
        quat = D3DXQUATERNION()
        d3dxdll.D3DXQuaternionRotationYawPitchRoll(byref(quat),
            c_float(rot[1]), c_float(rot[0]), c_float(rot[2]))
    
        vtrans = D3DVECTOR(*trans)
        vscale = D3DVECTOR(*scale)
        matrix = D3DMATRIX()
        d3dxdll.D3DXMatrixTransformation(byref(matrix), None, 
            None, byref(vscale), None, byref(quat), byref(vtrans))

        self.device.SetTransform(D3DTS.WORLD, byref(matrix))
    
    def SetView(self, eye, lookat):
        """Same as in DirectPython."""
        view = D3DMATRIX()
        up = D3DVECTOR(0, 1, 0)
        eye = D3DVECTOR(*eye)
        lookat = D3DVECTOR(*lookat)
        d3dxdll.D3DXMatrixLookAtLH(byref(view), byref(eye), 
            byref(lookat), byref(up))
        self.device.SetTransform(D3DTS.VIEW, byref(view))
        
        aspect = c_float(float(self.presentparams.BackBufferWidth) / 
            max(self.presentparams.BackBufferHeight, 1))
        
        proj = D3DMATRIX()
        d3dxdll.D3DXMatrixPerspectiveFovLH(byref(proj), 
            c_float(3.14 / 4), aspect, c_float(0.5), c_float(300.0))
        self.device.SetTransform(D3DTS.PROJECTION, byref(proj))
    
    def ResetDevice(self):
        """Attempts to reset the device. 
           Mostly called internally."""
        self.Pause(True)
        
        self.OnLostDevice()
        self.font.OnLostDevice()
        
        #Make sure that the message proc can't 
        #recall this method while it's still executing.
        Frame._activeframe = None
        
        while 1:
            try:
                client = RECT()
                windll.user32.GetClientRect(self.hwnd, byref(client))
                
                self.presentparams.BackBufferWidth = client.right 
                self.presentparams.BackBufferHeight = client.bottom 
                self.presentparams.Windowed = not self.fullscreen
                
                oldformat = self.presentparams.BackBufferFormat
                
                #XXX - should check for internal errors.
                self.device.Reset(byref(self.presentparams))
                
                self.presentparams.BackBufferFormat = oldformat
                
                break #Succeeded, break out.
            except:
                #Failed, handle messages and wait.
                self.ProcessMessages()
                time.sleep(0.1)
                
        Frame._activeframe = self
                     
        self.font.OnResetDevice()
        self.OnResetDevice()
        
        self.Pause(False)
        self.OnUpdate()
            
    def IsPaused(self):
        """Returns True if the Frame is currently paused."""
        return self._pauses > 0
            
    def Pause(self, yes):
        """Pauses or unpauses the application. Multiple
           levels of pausing are remembered and the
           application will remain paused until
           all pauses have been unpaused. When the application
           is paused, the time does not advance and most 
           callbacks are not called. """
        if yes:
            self._pauses += 1
            if self._pauses == 1:
                #First pause.
                self._pausestart = time.clock()
        else:
            self._pauses -= 1
            if self._pauses == 0:
                #No longer paused.
                self._pausetime += time.clock() - self._pausestart 

        assert (self._pauses >= 0)
            
    def ToggleFullscreen(self):
        """Toggles between windowed and fullscreen modes."""
        if self.fullscreen:
            #To windowed mode
            result = RECT(200, 100, 800, 600)
            windll.user32.AdjustWindowRect(byref(result), DWORD(WINDOWED), BOOL(0))
            windll.user32.SetWindowLongA(self.hwnd, INT(-16), INT(WINDOWED))
            windll.user32.SetWindowPos(self.hwnd, HWND(0), result.left, result.top, 
                result.right, result.bottom, 0x0020)    
        else:
            #To fullscreen mode.
            windll.user32.SetWindowLongA(self.hwnd, INT(-16), INT(FULLSCREEN))
            windll.user32.SetWindowPos(self.hwnd, HWND(0), 0, 0, 
                self.fullscreenres[0], self.fullscreenres[1], 0x0020)
           
        self.fullscreen = not self.fullscreen
        
        if self.device is None:
            self.CreateDevice()
        else:
            self.ResetDevice()
        
        self.OnUpdate()
    
        #Show our window and refresh all other windows.
        windll.user32.ShowWindow(self.hwnd, c_int(1))
        windll.user32.InvalidateRect(HWND(0), None, BOOL(0))
    
    def OnCreateDevice(self):
        """Called when a new device has been created. All
           Direct3D resources can be created in here."""
        pass
    
    def OnDestroyDevice(self):
        """Called when the device will soon be destroyed. All
           Direct3D resources should be destroyed in here."""
        pass
    
    def OnLostDevice(self):
        """Called before the device is reset. Any DEFAUL-pool
           resources should be released in here."""
        pass
    
    def OnResetDevice(self):
        """Called after the device has been reset. Any DEFAUL-pool
           resources should be re-created in here."""
        pass
    
    def OnUpdate(self):
        """Called once per frame (if not paused) or when the 
           scene needs to be updated."""
        pass
    
    def OnRender(self):
        """Called once per frame, even if paused."""
        pass
    
    def OnChar(self, char):
        """Called when a character key has been pressed."""
        pass
    
    def OnKey(self, msg):
        """Called when any key has been pressed."""
        pass
    
    def OnMouse(self, msg):
        """Called when a mouse event has occured."""
        pass
    
    def OnInit(self):
        """Called once during the startup. This method can
           perform all one-time initialization (altough it
           should not create any DirectX objects)."""
        pass
    
    def OnClose(self):
        """Called when the Frame is closing normally. This
           is the opposite of OnInit() and is also called once."""
        pass
    
_keyevents = (0x0101, 0x0100, 0x0104, 0x0105)
    
def _WndProc(hwnd, msg, wParam, lParam):
    """Normal Windows message procedure."""
    self = Frame._activeframe

    if self:
        args = (msg, wParam, lParam) 
    
        if self._hooks:
            for hook in self._hooks:
                if hook(hwnd, msg, wParam, lParam):
                    #Hook handled the message.
                    return 0
    
        if IsMouseMessage(msg):
            x = lParam & 0xffff
            y = lParam >> 16
            if msg == 0x0200: #WM_MOUSEMOVE
                self.device.SetCursorPosition(x, y, 0)
            elif msg == 0x020A: #WM_MOUSEWHEEL
                point = POINT(x, y)
                windll.user32.ScreenToClient(hwnd, byref(point));
                x = point.x
                y = point.y  
            self.OnMouse((msg, x, y))
            return 0
        elif msg == 0x0102:
            #WM_CHAR
            char = unichr(wParam)
            if char == u"p":
                #XXX - no respect for nesting pauses!
                assert (self._pauses == 0 or self._pauses == 1)
                self.Pause(not self._pauses) 
            else:
                self.OnChar(char)
            return 0
        elif msg in _keyevents:
            #We "steal" some panic keys.
            if msg == 0x0105: #System key down.
                if wParam == 0x79: #F10
                    self.ToggleFullscreen()
            elif msg == 0x0100: #Normal key down.
                if wParam == 0x1B: #Esc
                    #ctypes seems to respect SystemExit
                    #in callbacks?
                    self.Quit()
                elif wParam == 0x70: #F1
                    self.showhelp = not self.showhelp
                elif wParam == 0x77: #F8
                    if self._fillmode == D3DFILL.WIREFRAME:
                        self._fillmode = D3DFILL.SOLID
                    else:
                        self._fillmode = D3DFILL.WIREFRAME    
                else:
                    self.OnKey(args)  
            else:
                self.OnKey(args)
            return 0
        elif msg == 0x0084: 
            #WM_NCHITTEST
            if self.fullscreen:
                return 1 #Client area
        elif msg == 0x0005: 
            #WM_SIZE 
            if not self._resizing and not self.fullscreen:
                if wParam == 1: #Minimized
                    pass
                elif wParam == 2 or wParam == 0: #Maximized/Restored
                    self.ResetDevice()
                    return 0
        elif msg == 0x0231: 
            #WM_ENTERSIZEMOVE
            self._resizing = True 
            self.Pause(True)
            return 0
        elif msg == 0x0232: 
            #WM_EXITSIZEMOVE
            #XXX - currently resets even if only moved.
            self._resizing = False
            self.ResetDevice()
            self.Pause(False)
            return 0
        elif msg == 0x001C and self.fullscreen:
            #Lost focus in fullscreen.
            self.ToggleFullscreen()
            return 0

    if msg == 0x0112: 
        #WM_SYSCOMMAND
        if wParam == 0xF100: #SC_KEYMENU
            return 0    
    elif msg == 0x2:
        windll.user32.PostQuitMessage(0)
        return 0 
      
    return windll.user32.DefWindowProcA(HWND(hwnd), UINT(msg), WPARAM(wParam), LPARAM(lParam))
     
    