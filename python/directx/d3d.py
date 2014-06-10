
from directx.types import *

class IDirect3D9(IUnknown):
    _iid_ = GUID("{81BDCBCA-64D4-426d-AE8D-AD0147F4275C}")
    _methods_ = [
        STDMETHOD(HRESULT, 'RegisterSoftwareDevice', [POINTER(None)]),
        STDMETHOD(c_uint, 'GetAdapterCount'),
        STDMETHOD(HRESULT, 'GetAdapterIdentifier', [c_uint, DWORD, POINTER(D3DADAPTER_IDENTIFIER9)]),
        STDMETHOD(c_uint, 'GetAdapterModeCount', [c_uint, DWORD]),
        STDMETHOD(HRESULT, 'EnumAdapterModes', [c_uint, DWORD, c_uint, POINTER(D3DDISPLAYMODE)]),
        STDMETHOD(HRESULT, 'GetAdapterDisplayMode', [c_uint, POINTER(D3DDISPLAYMODE)]),
        STDMETHOD(HRESULT, 'CheckDeviceType', [c_uint, DWORD, DWORD, DWORD, BOOL]),
        STDMETHOD(HRESULT, 'CheckDeviceFormat', [c_uint, DWORD, DWORD, DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'CheckDeviceMultiSampleType', [c_uint, DWORD, DWORD, BOOL, DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'CheckDepthStencilMatch', [c_uint, DWORD, DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'CheckDeviceFormatConversion', [c_uint, DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'GetDeviceCaps', [c_uint, DWORD, POINTER(D3DCAPS9)]),
        STDMETHOD(HMONITOR, 'GetAdapterMonitor', [c_uint]),
        STDMETHOD(HRESULT, 'CreateDevice', [c_uint, DWORD, HWND, DWORD, POINTER(D3DPRESENT_PARAMETERS), POINTER(POINTER(None))]),
    ]

class IDirect3DDevice9(IUnknown):
    _iid_ = GUID("{D0223B96-BF7A-43fd-92BD-A43B0D82B9EB}")
    _methods_ = [
        STDMETHOD(HRESULT, 'TestCooperativeLevel'),
        STDMETHOD(c_uint, 'GetAvailableTextureMem'),
        STDMETHOD(HRESULT, 'EvictManagedResources'),
        STDMETHOD(HRESULT, 'GetDirect3D', [POINTER(POINTER(IDirect3D9))]),
        STDMETHOD(HRESULT, 'GetDeviceCaps', [POINTER(D3DCAPS9)]),
        STDMETHOD(HRESULT, 'GetDisplayMode', [c_uint, POINTER(D3DDISPLAYMODE)]),
        STDMETHOD(HRESULT, 'GetCreationParameters', [POINTER(D3DDEVICE_CREATION_PARAMETERS)]),
        STDMETHOD(HRESULT, 'SetCursorProperties', [c_uint, c_uint, POINTER(None)]),
        STDMETHOD(None, 'SetCursorPosition', [c_int, c_int, DWORD]),
        STDMETHOD(BOOL, 'ShowCursor', [BOOL]),
        STDMETHOD(HRESULT, 'CreateAdditionalSwapChain', [POINTER(D3DPRESENT_PARAMETERS), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'GetSwapChain', [c_uint, POINTER(POINTER(None))]),
        STDMETHOD(c_uint, 'GetNumberOfSwapChains'),
        STDMETHOD(HRESULT, 'Reset', [POINTER(D3DPRESENT_PARAMETERS)]),
        STDMETHOD(HRESULT, 'Present', [POINTER(RECT), POINTER(RECT), HWND, POINTER(RGNDATA)]),
        STDMETHOD(HRESULT, 'GetBackBuffer', [c_uint, c_uint, DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'GetRasterStatus', [c_uint, POINTER(D3DRASTER_STATUS)]),
        STDMETHOD(HRESULT, 'SetDialogBoxMode', [BOOL]),
        STDMETHOD(None, 'SetGammaRamp', [c_uint, DWORD, POINTER(D3DGAMMARAMP)]),
        STDMETHOD(None, 'GetGammaRamp', [c_uint, POINTER(D3DGAMMARAMP)]),
        STDMETHOD(HRESULT, 'CreateTexture', [c_uint, c_uint, c_uint, DWORD, DWORD, DWORD, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'CreateVolumeTexture', [c_uint, c_uint, c_uint, c_uint, DWORD, DWORD, DWORD, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'CreateCubeTexture', [c_uint, c_uint, DWORD, DWORD, DWORD, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'CreateVertexBuffer', [c_uint, DWORD, DWORD, DWORD, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'CreateIndexBuffer', [c_uint, DWORD, DWORD, DWORD, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'CreateRenderTarget', [c_uint, c_uint, DWORD, DWORD, DWORD, BOOL, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'CreateDepthStencilSurface', [c_uint, c_uint, DWORD, DWORD, DWORD, BOOL, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'UpdateSurface', [POINTER(None), POINTER(RECT), POINTER(None), POINTER(POINT)]),
        STDMETHOD(HRESULT, 'UpdateTexture', [POINTER(None), POINTER(None)]),
        STDMETHOD(HRESULT, 'GetRenderTargetData', [POINTER(None), POINTER(None)]),
        STDMETHOD(HRESULT, 'GetFrontBufferData', [c_uint, POINTER(None)]),
        STDMETHOD(HRESULT, 'StretchRect', [POINTER(None), POINTER(RECT), POINTER(None), POINTER(RECT), DWORD]),
        STDMETHOD(HRESULT, 'ColorFill', [POINTER(None), POINTER(RECT), DWORD]),
        STDMETHOD(HRESULT, 'CreateOffscreenPlainSurface', [c_uint, c_uint, DWORD, DWORD, POINTER(POINTER(None)), POINTER(HANDLE)]),
        STDMETHOD(HRESULT, 'SetRenderTarget', [DWORD, POINTER(None)]),
        STDMETHOD(HRESULT, 'GetRenderTarget', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetDepthStencilSurface', [POINTER(None)]),
        STDMETHOD(HRESULT, 'GetDepthStencilSurface', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'BeginScene'),
        STDMETHOD(HRESULT, 'EndScene'),
        STDMETHOD(HRESULT, 'Clear', [DWORD, POINTER(D3DRECT), DWORD, DWORD, c_float, DWORD]),
        STDMETHOD(HRESULT, 'SetTransform', [DWORD, POINTER(D3DMATRIX)]),
        STDMETHOD(HRESULT, 'GetTransform', [DWORD, POINTER(D3DMATRIX)]),
        STDMETHOD(HRESULT, 'MultiplyTransform', [DWORD, POINTER(D3DMATRIX)]),
        STDMETHOD(HRESULT, 'SetViewport', [POINTER(D3DVIEWPORT9)]),
        STDMETHOD(HRESULT, 'GetViewport', [POINTER(D3DVIEWPORT9)]),
        STDMETHOD(HRESULT, 'SetMaterial', [POINTER(D3DMATERIAL9)]),
        STDMETHOD(HRESULT, 'GetMaterial', [POINTER(D3DMATERIAL9)]),
        STDMETHOD(HRESULT, 'SetLight', [DWORD, POINTER(D3DLIGHT9)]),
        STDMETHOD(HRESULT, 'GetLight', [DWORD, POINTER(D3DLIGHT9)]),
        STDMETHOD(HRESULT, 'LightEnable', [DWORD, BOOL]),
        STDMETHOD(HRESULT, 'GetLightEnable', [DWORD, POINTER(BOOL)]),
        STDMETHOD(HRESULT, 'SetClipPlane', [DWORD, POINTER(c_float)]),
        STDMETHOD(HRESULT, 'GetClipPlane', [DWORD, POINTER(c_float)]),
        STDMETHOD(HRESULT, 'SetRenderState', [DWORD, DWORD]),
        STDMETHOD(HRESULT, 'GetRenderState', [DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'CreateStateBlock', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'BeginStateBlock'),
        STDMETHOD(HRESULT, 'EndStateBlock', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetClipStatus', [POINTER(D3DCLIPSTATUS9)]),
        STDMETHOD(HRESULT, 'GetClipStatus', [POINTER(D3DCLIPSTATUS9)]),
        STDMETHOD(HRESULT, 'GetTexture', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetTexture', [DWORD, POINTER(None)]),
        STDMETHOD(HRESULT, 'GetTextureStageState', [DWORD, DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'SetTextureStageState', [DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'GetSamplerState', [DWORD, DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'SetSamplerState', [DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'ValidateDevice', [POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'SetPaletteEntries', [c_uint, POINTER(PALETTEENTRY)]),
        STDMETHOD(HRESULT, 'GetPaletteEntries', [c_uint, POINTER(PALETTEENTRY)]),
        STDMETHOD(HRESULT, 'SetCurrentTexturePalette', [c_uint]),
        STDMETHOD(HRESULT, 'GetCurrentTexturePalette', [POINTER(c_uint)]),
        STDMETHOD(HRESULT, 'SetScissorRect', [POINTER(RECT)]),
        STDMETHOD(HRESULT, 'GetScissorRect', [POINTER(RECT)]),
        STDMETHOD(HRESULT, 'SetSoftwareVertexProcessing', [BOOL]),
        STDMETHOD(BOOL, 'GetSoftwareVertexProcessing'),
        STDMETHOD(HRESULT, 'SetNPatchMode', [c_float]),
        STDMETHOD(c_float, 'GetNPatchMode'),
        STDMETHOD(HRESULT, 'DrawPrimitive', [DWORD, c_uint, c_uint]),
        STDMETHOD(HRESULT, 'DrawIndexedPrimitive', [DWORD, INT, c_uint, c_uint, c_uint, c_uint]),
        STDMETHOD(HRESULT, 'DrawPrimitiveUP', [DWORD, c_uint, POINTER(None), c_uint]),
        STDMETHOD(HRESULT, 'DrawIndexedPrimitiveUP', [DWORD, c_uint, c_uint, c_uint, POINTER(None), DWORD, POINTER(None), c_uint]),
        STDMETHOD(HRESULT, 'ProcessVertices', [c_uint, c_uint, c_uint, POINTER(None), POINTER(None), DWORD]),
        STDMETHOD(HRESULT, 'CreateVertexDeclaration', [POINTER(D3DVERTEXELEMENT9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetVertexDeclaration', [POINTER(None)]),
        STDMETHOD(HRESULT, 'GetVertexDeclaration', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetFVF', [DWORD]),
        STDMETHOD(HRESULT, 'GetFVF', [POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'CreateVertexShader', [POINTER(DWORD), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetVertexShader', [POINTER(None)]),
        STDMETHOD(HRESULT, 'GetVertexShader', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetVertexShaderConstantF', [c_uint, POINTER(c_float), c_uint]),
        STDMETHOD(HRESULT, 'GetVertexShaderConstantF', [c_uint, POINTER(c_float), c_uint]),
        STDMETHOD(HRESULT, 'SetVertexShaderConstantI', [c_uint, POINTER(c_int), c_uint]),
        STDMETHOD(HRESULT, 'GetVertexShaderConstantI', [c_uint, POINTER(c_int), c_uint]),
        STDMETHOD(HRESULT, 'SetVertexShaderConstantB', [c_uint, POINTER(BOOL), c_uint]),
        STDMETHOD(HRESULT, 'GetVertexShaderConstantB', [c_uint, POINTER(BOOL), c_uint]),
        STDMETHOD(HRESULT, 'SetStreamSource', [c_uint, POINTER(None), c_uint, c_uint]),
        STDMETHOD(HRESULT, 'GetStreamSource', [c_uint, POINTER(POINTER(None)), POINTER(c_uint), POINTER(c_uint)]),
        STDMETHOD(HRESULT, 'SetStreamSourceFreq', [c_uint, c_uint]),
        STDMETHOD(HRESULT, 'GetStreamSourceFreq', [c_uint, POINTER(c_uint)]),
        STDMETHOD(HRESULT, 'SetIndices', [POINTER(None)]),
        STDMETHOD(HRESULT, 'GetIndices', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'CreatePixelShader', [POINTER(DWORD), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetPixelShader', [POINTER(None)]),
        STDMETHOD(HRESULT, 'GetPixelShader', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetPixelShaderConstantF', [c_uint, POINTER(c_float), c_uint]),
        STDMETHOD(HRESULT, 'GetPixelShaderConstantF', [c_uint, POINTER(c_float), c_uint]),
        STDMETHOD(HRESULT, 'SetPixelShaderConstantI', [c_uint, POINTER(c_int), c_uint]),
        STDMETHOD(HRESULT, 'GetPixelShaderConstantI', [c_uint, POINTER(c_int), c_uint]),
        STDMETHOD(HRESULT, 'SetPixelShaderConstantB', [c_uint, POINTER(BOOL), c_uint]),
        STDMETHOD(HRESULT, 'GetPixelShaderConstantB', [c_uint, POINTER(BOOL), c_uint]),
        STDMETHOD(HRESULT, 'DrawRectPatch', [c_uint, POINTER(c_float), POINTER(D3DRECTPATCH_INFO)]),
        STDMETHOD(HRESULT, 'DrawTriPatch', [c_uint, POINTER(c_float), POINTER(D3DTRIPATCH_INFO)]),
        STDMETHOD(HRESULT, 'DeletePatch', [c_uint]),
        STDMETHOD(HRESULT, 'CreateQuery', [DWORD, POINTER(POINTER(None))]),
    ]
    
class IDirect3DStateBlock9(IUnknown):
    _iid_ = GUID("{B07C4FE5-310D-4ba8-A23C-4F0F206F218B}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'Capture'),
        STDMETHOD(HRESULT, 'Apply'),
    ]
    
class IDirect3DResource9(IUnknown):
    _iid_ = GUID("{05EEC05D-8F7D-4362-B999-D1BAF357C704}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        STDMETHOD(DWORD, 'GetPriority'),
        STDMETHOD(None, 'PreLoad'),
        STDMETHOD(DWORD, 'GetType'),
    ]
    
class IDirect3DVertexDeclaration9(IUnknown):
    _iid_ = GUID("{DD13C59C-36FA-4098-A8FB-C7ED39DC8546}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetDeclaration', [POINTER(D3DVERTEXELEMENT9), POINTER(c_uint)]),
    ]
    
class IDirect3DVertexShader9(IUnknown):
    _iid_ = GUID("{EFC5557E-6265-4613-8A94-43857889EB36}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetFunction', [POINTER(None), POINTER(c_uint)]),
    ]
    
class IDirect3DPixelShader9(IUnknown):
    _iid_ = GUID("{6D3BDBDC-5B02-4415-B852-CE5E8BCCB289}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetFunction', [POINTER(None), POINTER(c_uint)]),
    ]
    
class IDirect3DBaseTexture9(IDirect3DResource9):
    _iid_ = GUID("{580CA87E-1D3C-4d54-991D-B7D3E3C298CE}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        STDMETHOD(DWORD, 'SetLOD', [DWORD]),
        STDMETHOD(DWORD, 'GetLOD'),
        STDMETHOD(DWORD, 'GetLevelCount'),
        STDMETHOD(HRESULT, 'SetAutoGenFilterType', [DWORD]),
        STDMETHOD(DWORD, 'GetAutoGenFilterType'),
        STDMETHOD(None, 'GenerateMipSubLevels'),
    ]
    
class IDirect3DTexture9(IDirect3DBaseTexture9):
    _iid_ = GUID("{85C31227-3DE5-4f00-9B3A-F11AC38C18B5}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        #STDMETHOD(DWORD, 'SetLOD', [DWORD]),
        #STDMETHOD(DWORD, 'GetLOD'),
        #STDMETHOD(DWORD, 'GetLevelCount'),
        #STDMETHOD(HRESULT, 'SetAutoGenFilterType', [DWORD]),
        #STDMETHOD(DWORD, 'GetAutoGenFilterType'),
        #STDMETHOD(None, 'GenerateMipSubLevels'),
        STDMETHOD(HRESULT, 'GetLevelDesc', [c_uint, POINTER(D3DSURFACE_DESC)]),
        STDMETHOD(HRESULT, 'GetSurfaceLevel', [c_uint, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'LockRect', [c_uint, POINTER(D3DLOCKED_RECT), POINTER(RECT), DWORD]),
        STDMETHOD(HRESULT, 'UnlockRect', [c_uint]),
        STDMETHOD(HRESULT, 'AddDirtyRect', [POINTER(RECT)]),
    ]
    
class IDirect3DVolumeTexture9(IDirect3DBaseTexture9):
    _iid_ = GUID("{2518526C-E789-4111-A7B9-47EF328D13E6}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        #STDMETHOD(DWORD, 'SetLOD', [DWORD]),
        #STDMETHOD(DWORD, 'GetLOD'),
        #STDMETHOD(DWORD, 'GetLevelCount'),
        #STDMETHOD(HRESULT, 'SetAutoGenFilterType', [DWORD]),
        #STDMETHOD(DWORD, 'GetAutoGenFilterType'),
        #STDMETHOD(None, 'GenerateMipSubLevels'),
        STDMETHOD(HRESULT, 'GetLevelDesc', [c_uint, POINTER(D3DVOLUME_DESC)]),
        STDMETHOD(HRESULT, 'GetVolumeLevel', [c_uint, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'LockBox', [c_uint, POINTER(D3DLOCKED_BOX), POINTER(D3DBOX), DWORD]),
        STDMETHOD(HRESULT, 'UnlockBox', [c_uint]),
        STDMETHOD(HRESULT, 'AddDirtyBox', [POINTER(D3DBOX)]),
    ]
    
class IDirect3DCubeTexture9(IDirect3DBaseTexture9):
    _iid_ = GUID("{FFF32F81-D953-473a-9223-93D652ABA93F}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        #STDMETHOD(DWORD, 'SetLOD', [DWORD]),
        #STDMETHOD(DWORD, 'GetLOD'),
        #STDMETHOD(DWORD, 'GetLevelCount'),
        #STDMETHOD(HRESULT, 'SetAutoGenFilterType', [DWORD]),
        #STDMETHOD(DWORD, 'GetAutoGenFilterType'),
        #STDMETHOD(None, 'GenerateMipSubLevels'),
        STDMETHOD(HRESULT, 'GetLevelDesc', [c_uint, POINTER(D3DSURFACE_DESC)]),
        STDMETHOD(HRESULT, 'GetCubeMapSurface', [DWORD, c_uint, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'LockRect', [DWORD, c_uint, POINTER(D3DLOCKED_RECT), POINTER(RECT), DWORD]),
        STDMETHOD(HRESULT, 'UnlockRect', [DWORD, c_uint]),
        STDMETHOD(HRESULT, 'AddDirtyRect', [DWORD, POINTER(RECT)]),
    ]
    
class IDirect3DVertexBuffer9(IDirect3DResource9):
    _iid_ = GUID("{B64BB1B5-FD70-4df6-BF91-19D0A12455E3}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        STDMETHOD(HRESULT, 'Lock', [c_uint, c_uint, POINTER(POINTER(None)), DWORD]),
        STDMETHOD(HRESULT, 'Unlock'),
        STDMETHOD(HRESULT, 'GetDesc', [POINTER(D3DVERTEXBUFFER_DESC)]),
    ]
    
class IDirect3DIndexBuffer9(IDirect3DResource9):
    _iid_ = GUID("{7C9DD65E-D3F7-4529-ACEE-785830ACDE35}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        STDMETHOD(HRESULT, 'Lock', [c_uint, c_uint, POINTER(POINTER(None)), DWORD]),
        STDMETHOD(HRESULT, 'Unlock'),
        STDMETHOD(HRESULT, 'GetDesc', [POINTER(D3DINDEXBUFFER_DESC)]),
    ]
    
class IDirect3DSurface9(IDirect3DResource9):
    _iid_ = GUID("{0CFBAF3A-9FF6-429a-99B3-A2796AF8B89B}")
    _methods_ = [
        #STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        #STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        #STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        #STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        #STDMETHOD(DWORD, 'SetPriority', [DWORD]),
        #STDMETHOD(DWORD, 'GetPriority'),
        #STDMETHOD(None, 'PreLoad'),
        #STDMETHOD(DWORD, 'GetType'),
        STDMETHOD(HRESULT, 'GetContainer', [POINTER(GUID), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'GetDesc', [POINTER(D3DSURFACE_DESC)]),
        STDMETHOD(HRESULT, 'LockRect', [POINTER(D3DLOCKED_RECT), POINTER(RECT), DWORD]),
        STDMETHOD(HRESULT, 'UnlockRect'),
        STDMETHOD(HRESULT, 'GetDC', [POINTER(HDC)]),
        STDMETHOD(HRESULT, 'ReleaseDC', [HDC]),
    ]
    
class IDirect3DVolume9(IUnknown):
    _iid_ = GUID("{24F416E6-1F67-4aa7-B88E-D33F6F3128A1}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'SetPrivateData', [POINTER(GUID), POINTER(None), DWORD, DWORD]),
        STDMETHOD(HRESULT, 'GetPrivateData', [POINTER(GUID), POINTER(None), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'FreePrivateData', [POINTER(GUID)]),
        STDMETHOD(HRESULT, 'GetContainer', [POINTER(GUID), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'GetDesc', [POINTER(D3DVOLUME_DESC)]),
        STDMETHOD(HRESULT, 'LockBox', [POINTER(D3DLOCKED_BOX), POINTER(D3DBOX), DWORD]),
        STDMETHOD(HRESULT, 'UnlockBox'),
    ]
    
class IDirect3DSwapChain9(IUnknown):
    _iid_ = GUID("{794950F2-ADFC-458a-905E-10A10B0B503B}")
    _methods_ = [
        STDMETHOD(HRESULT, 'Present', [POINTER(RECT), POINTER(RECT), HWND, POINTER(RGNDATA), DWORD]),
        STDMETHOD(HRESULT, 'GetFrontBufferData', [POINTER(IDirect3DSurface9)]),
        STDMETHOD(HRESULT, 'GetBackBuffer', [c_uint, DWORD, POINTER(POINTER(IDirect3DSurface9))]),
        STDMETHOD(HRESULT, 'GetRasterStatus', [POINTER(D3DRASTER_STATUS)]),
        STDMETHOD(HRESULT, 'GetDisplayMode', [POINTER(D3DDISPLAYMODE)]),
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetPresentParameters', [POINTER(D3DPRESENT_PARAMETERS)]),
    ]
    
class IDirect3DQuery9(IUnknown):
    _iid_ = GUID("{d9771460-a695-4f26-bbd3-27b840b541cc}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(DWORD, 'GetType'),
        STDMETHOD(DWORD, 'GetDataSize'),
        STDMETHOD(HRESULT, 'Issue', [DWORD]),
        STDMETHOD(HRESULT, 'GetData', [POINTER(None), DWORD, DWORD]),
    ]
    