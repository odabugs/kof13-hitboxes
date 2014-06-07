
from directx.types import *
from directx.d3d import *

#********************************************************************
#   Typedefs and constants
#********************************************************************

try:
    #SDK April 2006 - you can change the
    #.dll to a another one if you know what you are doing.
    if D3DDEBUGENABLED:
        print "Debugging enabled, attempting to load the debug D3DX .dll"
        d3dxdll = windll.d3dx9d_30
    else:
        d3dxdll = windll.d3dx9_30
except:
    print """
    *****************************************************
    You don't seem to have the D3D end-user runtime installed. 
    Visit Microsoft's DirectX web site for latest downloads.
    ***************************************************** 
    """
    raise

D3DX_VERSION = 0x0902
D3DX_SDK_VERSION = 30

D3DXMATRIX = D3DMATRIX
D3DXVECTOR3 = D3DVECTOR
D3DXHANDLE = LPCSTR
   
#********************************************************************
#   Functions
#********************************************************************

def TestHR(hr):
    if hr < 0:
        #Todo: create a wrapper for Dxerr.lib (normal HR lookups
        #can be wrong and thus confusing).
        raise WinError("Unknown error (not yet implemented)", -1)
    else:
        return hr

#********************************************************************
#   Interfaces
#******************************************************************** 
        
class ID3DXBuffer(IUnknown):
    _iid_ = GUID("{8BA5FB08-5195-40e2-AC58-0D989C3A0102}")
    _methods_ = [
        STDMETHOD(POINTER(None), 'GetBufferPointer'),
        STDMETHOD(DWORD, 'GetBufferSize'),
    ]

class ID3DXSprite(IUnknown):
    _iid_ = GUID("{BA0B762D-7D28-43ec-B9DC-2F84443B0614}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetTransform', [POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'SetTransform', [POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'SetWorldViewRH', [POINTER(D3DXMATRIX), POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'SetWorldViewLH', [POINTER(D3DXMATRIX), POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'Begin', [DWORD]),
        STDMETHOD(HRESULT, 'Draw', [POINTER(IDirect3DTexture9), POINTER(RECT), POINTER(D3DXVECTOR3), POINTER(D3DXVECTOR3), DWORD]),
        STDMETHOD(HRESULT, 'Flush'),
        STDMETHOD(HRESULT, 'End'),
        STDMETHOD(HRESULT, 'OnLostDevice'),
        STDMETHOD(HRESULT, 'OnResetDevice'),
    ]

class ID3DXFont(IUnknown):
    _iid_ = GUID("{D79DBB70-5F21-4d36-BBC2-FF525C213CDC}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetDescAXXX', [POINTER(None)]), #Todo
        STDMETHOD(HRESULT, 'GetDescW', [POINTER(D3DXFONT_DESCW)]),
        STDMETHOD(BOOL, 'GetTextMetricsAXXX', [POINTER(None)]), #Todo
        STDMETHOD(BOOL, 'GetTextMetricsW', [POINTER(TEXTMETRICW)]),
        STDMETHOD(HDC, 'GetDC'),
        STDMETHOD(HRESULT, 'GetGlyphData', [UINT, POINTER(IDirect3DTexture9), POINTER(RECT), POINTER(POINT)]),
        STDMETHOD(HRESULT, 'PreloadCharacters', [UINT, UINT]),
        STDMETHOD(HRESULT, 'PreloadGlyphs', [UINT, UINT]),
        STDMETHOD(HRESULT, 'PreloadTextA', [LPCSTR, INT]),
        STDMETHOD(HRESULT, 'PreloadTextW', [LPCWSTR, INT]),
        STDMETHOD(INT, 'DrawTextA', [POINTER(ID3DXSprite), LPCSTR, INT, POINTER(RECT), DWORD, DWORD]),
        STDMETHOD(INT, 'DrawTextW', [POINTER(ID3DXSprite), LPCWSTR, INT, POINTER(RECT), DWORD, DWORD]),
        STDMETHOD(HRESULT, 'OnLostDevice'),
        STDMETHOD(HRESULT, 'OnResetDevice'),
    ]

class ID3DXLine(IUnknown):
    _iid_ = GUID("{D379BA7F-9042-4ac4-9F5E-58192A4C6BD8}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'Begin'),
        STDMETHOD(HRESULT, 'Draw', [POINTER(D3DXVECTOR2), DWORD, DWORD]),
        STDMETHOD(HRESULT, 'DrawTransform', [POINTER(D3DXVECTOR3), DWORD, POINTER(D3DMATRIX), DWORD]),
        STDMETHOD(HRESULT, 'SetPattern', [DWORD]),
        STDMETHOD(DWORD, 'GetPattern'),
        STDMETHOD(HRESULT, 'SetPatternScale', [c_float]),
        STDMETHOD(c_float, 'GetPatternScale'),
        STDMETHOD(HRESULT, 'SetWidth', [c_float]),
        STDMETHOD(c_float, 'GetWidth'),
        STDMETHOD(HRESULT, 'SetAntialias', [BOOL]),
        STDMETHOD(BOOL, 'GetAntialias'),
        STDMETHOD(HRESULT, 'SetGLLines', [BOOL]),
        STDMETHOD(BOOL, 'GetGLLines'),
        STDMETHOD(HRESULT, 'End'),
        STDMETHOD(HRESULT, 'OnLostDevice'),
        STDMETHOD(HRESULT, 'OnResetDevice'),
    ]
    
#********************************************************************
#   Interfaces (Effect)
#********************************************************************

class ID3DXEffectPool(IUnknown):
    _iid_ = GUID("{9537AB04-3250-412e-8213-FCD2F8677933}")
    _methods_ = [
    
    ]
    
class ID3DXBaseEffect(IUnknown):
    _iid_ = GUID("{017C18AC-103F-4417-8C51-6BF6EF1E56BE}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetDesc', [POINTER(D3DXEFFECT_DESC)]),
        STDMETHOD(HRESULT, 'GetParameterDesc', [D3DXHANDLE, POINTER(D3DXPARAMETER_DESC)]),
        STDMETHOD(HRESULT, 'GetTechniqueDesc', [D3DXHANDLE, POINTER(D3DXTECHNIQUE_DESC)]),
        STDMETHOD(HRESULT, 'GetPassDesc', [D3DXHANDLE, POINTER(D3DXPASS_DESC)]),
        STDMETHOD(HRESULT, 'GetFunctionDesc', [D3DXHANDLE, POINTER(D3DXFUNCTION_DESC)]),
        STDMETHOD(D3DXHANDLE, 'GetParameter', [D3DXHANDLE, UINT]),
        STDMETHOD(D3DXHANDLE, 'GetParameterByName', [D3DXHANDLE, LPCSTR]),
        STDMETHOD(D3DXHANDLE, 'GetParameterBySemantic', [D3DXHANDLE, LPCSTR]),
        STDMETHOD(D3DXHANDLE, 'GetParameterElement', [D3DXHANDLE, UINT]),
        STDMETHOD(D3DXHANDLE, 'GetTechnique', [UINT]),
        STDMETHOD(D3DXHANDLE, 'GetTechniqueByName', [LPCSTR]),
        STDMETHOD(D3DXHANDLE, 'GetPass', [D3DXHANDLE, UINT]),
        STDMETHOD(D3DXHANDLE, 'GetPassByName', [D3DXHANDLE, LPCSTR]),
        STDMETHOD(D3DXHANDLE, 'GetFunction', [UINT]),
        STDMETHOD(D3DXHANDLE, 'GetFunctionByName', [LPCSTR]),
        STDMETHOD(D3DXHANDLE, 'GetAnnotation', [D3DXHANDLE, UINT]),
        STDMETHOD(D3DXHANDLE, 'GetAnnotationByName', [D3DXHANDLE, LPCSTR]),
        STDMETHOD(HRESULT, 'SetValue', [D3DXHANDLE, POINTER(None), UINT]),
        STDMETHOD(HRESULT, 'GetValue', [D3DXHANDLE, POINTER(None), UINT]),
        STDMETHOD(HRESULT, 'SetBool', [D3DXHANDLE, BOOL]),
        STDMETHOD(HRESULT, 'GetBool', [D3DXHANDLE, POINTER(BOOL)]),
        STDMETHOD(HRESULT, 'SetBoolArray', [D3DXHANDLE, POINTER(BOOL), UINT]),
        STDMETHOD(HRESULT, 'GetBoolArray', [D3DXHANDLE, POINTER(BOOL), UINT]),
        STDMETHOD(HRESULT, 'SetInt', [D3DXHANDLE, INT]),
        STDMETHOD(HRESULT, 'GetInt', [D3DXHANDLE, POINTER(INT)]),
        STDMETHOD(HRESULT, 'SetIntArray', [D3DXHANDLE, POINTER(INT), UINT]),
        STDMETHOD(HRESULT, 'GetIntArray', [D3DXHANDLE, POINTER(INT), UINT]),
        STDMETHOD(HRESULT, 'SetFloat', [D3DXHANDLE, c_float]),
        STDMETHOD(HRESULT, 'GetFloat', [D3DXHANDLE, POINTER(c_float)]),
        STDMETHOD(HRESULT, 'SetFloatArray', [D3DXHANDLE, POINTER(c_float), UINT]),
        STDMETHOD(HRESULT, 'GetFloatArray', [D3DXHANDLE, POINTER(c_float), UINT]),
        STDMETHOD(HRESULT, 'SetVector', [D3DXHANDLE, POINTER(D3DXVECTOR4)]),
        STDMETHOD(HRESULT, 'GetVector', [D3DXHANDLE, POINTER(D3DXVECTOR4)]),
        STDMETHOD(HRESULT, 'SetVectorArray', [D3DXHANDLE, POINTER(D3DXVECTOR4), UINT]),
        STDMETHOD(HRESULT, 'GetVectorArray', [D3DXHANDLE, POINTER(D3DXVECTOR4), UINT]),
        STDMETHOD(HRESULT, 'SetMatrix', [D3DXHANDLE, POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'GetMatrix', [D3DXHANDLE, POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'SetMatrixArray', [D3DXHANDLE, POINTER(D3DXMATRIX), UINT]),
        STDMETHOD(HRESULT, 'GetMatrixArray', [D3DXHANDLE, POINTER(D3DXMATRIX), UINT]),
        STDMETHOD(HRESULT, 'SetMatrixPointerArray', [D3DXHANDLE, POINTER(POINTER(D3DXMATRIX)), UINT]),
        STDMETHOD(HRESULT, 'GetMatrixPointerArray', [D3DXHANDLE, POINTER(POINTER(D3DXMATRIX)), UINT]),
        STDMETHOD(HRESULT, 'SetMatrixTranspose', [D3DXHANDLE, POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'GetMatrixTranspose', [D3DXHANDLE, POINTER(D3DXMATRIX)]),
        STDMETHOD(HRESULT, 'SetMatrixTransposeArray', [D3DXHANDLE, POINTER(D3DXMATRIX), UINT]),
        STDMETHOD(HRESULT, 'GetMatrixTransposeArray', [D3DXHANDLE, POINTER(D3DXMATRIX), UINT]),
        STDMETHOD(HRESULT, 'SetMatrixTransposePointerArray', [D3DXHANDLE, POINTER(POINTER(D3DXMATRIX)), UINT]),
        STDMETHOD(HRESULT, 'GetMatrixTransposePointerArray', [D3DXHANDLE, POINTER(POINTER(D3DXMATRIX)), UINT]),
        STDMETHOD(HRESULT, 'SetString', [D3DXHANDLE, LPCSTR]),
        STDMETHOD(HRESULT, 'GetString', [D3DXHANDLE, POINTER(LPCSTR)]),
        STDMETHOD(HRESULT, 'SetTexture', [D3DXHANDLE, POINTER(IDirect3DBaseTexture9)]),
        STDMETHOD(HRESULT, 'GetTexture', [D3DXHANDLE, POINTER(IDirect3DBaseTexture9)]),
        STDMETHOD(HRESULT, 'GetPixelShader', [D3DXHANDLE, POINTER(IDirect3DPixelShader9)]),
        STDMETHOD(HRESULT, 'GetVertexShader', [D3DXHANDLE, POINTER(IDirect3DVertexShader9)]),
        STDMETHOD(HRESULT, 'SetArrayRange', [D3DXHANDLE, UINT, UINT]),
    ]

class ID3DXEffectStateManager(IUnknown):
    _iid_ = GUID("{79AAB587-6DBC-4fa7-82DE-37FA1781C5CE}")
    _methods_ = [
        STDMETHOD(HRESULT, 'SetTransform', [DWORD, POINTER(D3DMATRIX)]),
        STDMETHOD(HRESULT, 'SetMaterial', [D3DMATERIAL9]),
        STDMETHOD(HRESULT, 'SetLight', [DWORD, D3DLIGHT9]),
        STDMETHOD(HRESULT, 'LightEnable', [DWORD, BOOL]),
        STDMETHOD(HRESULT, 'SetRenderState', [DWORD, DWORD]),
        STDMETHOD(HRESULT, 'SetTexture', [DWORD, POINTER(IDirect3DBaseTexture9)]),
        STDMETHOD(HRESULT, 'SetTextureStageState', [DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'SetSamplerState', [DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'SetNPatchMode', [c_float]),
        STDMETHOD(HRESULT, 'SetFVF', [DWORD]),
        STDMETHOD(HRESULT, 'SetVertexShader', [POINTER(IDirect3DVertexShader9)]),
        STDMETHOD(HRESULT, 'SetVertexShaderConstantF', [UINT, c_float, UINT]),
        STDMETHOD(HRESULT, 'SetVertexShaderConstantI', [UINT, INT, UINT]),
        STDMETHOD(HRESULT, 'SetVertexShaderConstantB', [UINT, BOOL, UINT]),
        STDMETHOD(HRESULT, 'SetPixelShader', [POINTER(IDirect3DPixelShader9)]),
        STDMETHOD(HRESULT, 'SetPixelShaderConstantF', [UINT, c_float, UINT]),
        STDMETHOD(HRESULT, 'SetPixelShaderConstantI', [UINT, INT, UINT]),
        STDMETHOD(HRESULT, 'SetPixelShaderConstantB', [UINT, BOOL, UINT]),
    ]
    
class ID3DXEffect(ID3DXBaseEffect):
    _iid_ = GUID("{F6CEB4B3-4E4C-40dd-B883-8D8DE5EA0CD5}")
    _methods_ = [
        STDMETHOD(HRESULT, 'GetPool', [POINTER(ID3DXEffectPool)]),
        STDMETHOD(HRESULT, 'SetTechnique', [D3DXHANDLE]),
        STDMETHOD(D3DXHANDLE, 'GetCurrentTechnique'),
        STDMETHOD(HRESULT, 'ValidateTechnique', [D3DXHANDLE]),
        STDMETHOD(HRESULT, 'FindNextValidTechnique', [D3DXHANDLE, D3DXHANDLE]),
        STDMETHOD(BOOL, 'IsParameterUsed', [D3DXHANDLE, D3DXHANDLE]),
        STDMETHOD(HRESULT, 'Begin', [POINTER(UINT), DWORD]),
        STDMETHOD(HRESULT, 'BeginPass', [UINT]),
        STDMETHOD(HRESULT, 'CommitChanges'),
        STDMETHOD(HRESULT, 'EndPass'),
        STDMETHOD(HRESULT, 'End'),
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'OnLostDevice'),
        STDMETHOD(HRESULT, 'OnResetDevice'),
        STDMETHOD(HRESULT, 'SetStateManager', [POINTER(ID3DXEffectStateManager)]),
        STDMETHOD(HRESULT, 'GetStateManager', [POINTER(POINTER(ID3DXEffectStateManager))]),
        STDMETHOD(HRESULT, 'BeginParameterBlock'),
        STDMETHOD(D3DXHANDLE, 'EndParameterBlock'),
        STDMETHOD(HRESULT, 'ApplyParameterBlock', [D3DXHANDLE]),
        STDMETHOD(HRESULT, 'DeleteParameterBlock', [D3DXHANDLE]),
        STDMETHOD(HRESULT, 'CloneEffect', [POINTER(IDirect3DDevice9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetRawValue', [D3DXHANDLE, POINTER(None), UINT, UINT]),
    ]

class ID3DXEffectCompiler(ID3DXBaseEffect):
    _iid_ = GUID("{51B8A949-1A31-47e6-BEA0-4B30DB53F1E0}")
    _methods_ = [
        STDMETHOD(HRESULT, 'SetLiteral', [D3DXHANDLE, BOOL]),
        STDMETHOD(HRESULT, 'GetLiteral', [D3DXHANDLE, BOOL]),
        STDMETHOD(HRESULT, 'CompileEffect'),
        STDMETHOD(HRESULT, 'CompileShader'),
    ]    
    
#********************************************************************
#   Interfaces (Mesh)
#********************************************************************
    
class ID3DXBaseMesh(IUnknown):
    _iid_ = GUID("{7ED943DD-52E8-40b5-A8D8-76685C406330}")
    _methods_ = [
        STDMETHOD(HRESULT, 'DrawSubset', [DWORD]),
        STDMETHOD(DWORD, 'GetNumFaces'),
        STDMETHOD(DWORD, 'GetNumVertices'),
        STDMETHOD(DWORD, 'GetFVF'),
        STDMETHOD(HRESULT, 'GetDeclaration', [POINTER(D3DVERTEXELEMENT9)]),
        STDMETHOD(DWORD, 'GetNumBytesPerVertex'),
        STDMETHOD(DWORD, 'GetOptions'),
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'CloneMeshFVF', [DWORD, DWORD, POINTER(IDirect3DDevice9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'CloneMesh', [DWORD, POINTER(D3DVERTEXELEMENT9), POINTER(IDirect3DDevice9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'GetVertexBuffer', [POINTER(POINTER(IDirect3DVertexBuffer9))]),
        STDMETHOD(HRESULT, 'GetIndexBuffer', [POINTER(POINTER(IDirect3DIndexBuffer9))]),
        STDMETHOD(HRESULT, 'LockVertexBuffer', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'UnlockVertexBuffer'),
        STDMETHOD(HRESULT, 'LockIndexBuffer', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'UnlockIndexBuffer'),
        STDMETHOD(HRESULT, 'GetAttributeTable', [POINTER(D3DXATTRIBUTERANGE), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'ConvertPointRepsToAdjacency', [POINTER(DWORD), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'ConvertAdjacencyToPointReps', [POINTER(DWORD), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'GenerateAdjacency', [c_float, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'UpdateSemantics', [POINTER(D3DVERTEXELEMENT9)]),
    ]

class ID3DXMesh(ID3DXBaseMesh):
    _iid_ = GUID("{4020E5C2-1403-4929-883F-E2E849FAC195}")
    _methods_ = [
        STDMETHOD(HRESULT, 'LockAttributeBuffer', [DWORD, POINTER(POINTER(DWORD))]),
        STDMETHOD(HRESULT, 'UnlockAttributeBuffer'),
        STDMETHOD(HRESULT, 'Optimize', [DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXBuffer)), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'OptimizeInplace', [DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXBuffer))]),
        STDMETHOD(HRESULT, 'SetAttributeTable', [POINTER(D3DXATTRIBUTERANGE), DWORD]),
    ]
    
class ID3DXPMesh(ID3DXBaseMesh):
    _iid_ = GUID("{8875769A-D579-4088-AAEB-534D1AD84E96}")
    _methods_ = [
        STDMETHOD(HRESULT, 'ClonePMeshFVF', [DWORD, DWORD, POINTER(IDirect3DDevice9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'ClonePMesh', [DWORD, POINTER(D3DVERTEXELEMENT9), POINTER(IDirect3DDevice9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'SetNumFaces', [DWORD]),
        STDMETHOD(HRESULT, 'SetNumVertices', [DWORD]),
        STDMETHOD(DWORD, 'GetMaxFaces'),
        STDMETHOD(DWORD, 'GetMinFaces'),
        STDMETHOD(DWORD, 'GetMaxVertices'),
        STDMETHOD(DWORD, 'GetMinVertices'),
        STDMETHOD(HRESULT, 'Save', [POINTER(None), POINTER(D3DXMATERIAL), POINTER(None), DWORD]),
        STDMETHOD(HRESULT, 'Optimize', [DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXBuffer)), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'OptimizeBaseLOD', [DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'TrimByFaces', [DWORD, DWORD, POINTER(DWORD), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'TrimByVertices', [DWORD, DWORD, POINTER(DWORD), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'GetAdjacency', [POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'GenerateVertexHistory', [POINTER(DWORD)]),
    ]
    
class ID3DXSPMesh(IUnknown):
    _iid_ = GUID("{667EA4C7-F1CD-4386-B523-7C0290B83CC5}")
    _methods_ = [
        STDMETHOD(DWORD, 'GetNumFaces'),
        STDMETHOD(DWORD, 'GetNumVertices'),
        STDMETHOD(DWORD, 'GetFVF'),
        STDMETHOD(HRESULT, 'GetDeclaration', [POINTER(D3DVERTEXELEMENT9)]),
        STDMETHOD(DWORD, 'GetOptions'),
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'CloneMeshFVF', [DWORD, DWORD, POINTER(IDirect3DDevice9), POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXMesh))]),
        STDMETHOD(HRESULT, 'CloneMesh', [DWORD, POINTER(D3DVERTEXELEMENT9), POINTER(IDirect3DDevice9), POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXMesh))]),
        STDMETHOD(HRESULT, 'ClonePMeshFVF', [DWORD, DWORD, POINTER(D3DVERTEXELEMENT9), POINTER(DWORD), POINTER(c_float), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'ClonePMesh', [DWORD, POINTER(D3DVERTEXELEMENT9), POINTER(IDirect3DDevice9), POINTER(DWORD), POINTER(c_float), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'ReduceFaces', [DWORD]),
        STDMETHOD(HRESULT, 'ReduceVertices', [DWORD]),
        STDMETHOD(DWORD, 'GetMaxFaces'),
        STDMETHOD(DWORD, 'GetMaxVertices'),
        STDMETHOD(HRESULT, 'GetVertexAttributeWeights', [POINTER(D3DXATTRIBUTEWEIGHTS)]),
        STDMETHOD(HRESULT, 'GetVertexWeights', [c_float]),
    ]
    
class ID3DXSkinInfo(IUnknown):
    _iid_ = GUID("{11EAA540-F9A6-4d49-AE6A-E19221F70CC4}")
    _methods_ = [
        STDMETHOD(HRESULT, 'SetBoneInfluence', [DWORD, DWORD, POINTER(DWORD), POINTER(c_float)]),
        STDMETHOD(HRESULT, 'SetBoneVertexInfluence', [DWORD, DWORD, c_float]),
        STDMETHOD(DWORD, 'GetNumBoneInfluences', [DWORD]),
        STDMETHOD(HRESULT, 'GetBoneInfluence', [DWORD, POINTER(DWORD), POINTER(c_float)]),
        STDMETHOD(HRESULT, 'GetBoneVertexInfluence', [DWORD, DWORD, POINTER(c_float), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'GetMaxVertexInfluences', [POINTER(DWORD)]),
        STDMETHOD(DWORD, 'GetNumBones'),
        STDMETHOD(HRESULT, 'FindBoneVertexInfluenceIndex', [DWORD, DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'GetMaxFaceInfluences', [POINTER(IDirect3DIndexBuffer9), DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'SetMinBoneInfluence', [c_float]),
        STDMETHOD(c_float, 'GetMinBoneInfluence'),
        STDMETHOD(HRESULT, 'SetBoneName', [DWORD, LPCSTR]),
        STDMETHOD(LPCSTR, 'GetBoneName', [DWORD]),
        STDMETHOD(HRESULT, 'SetBoneOffsetMatrix', [DWORD, POINTER(D3DXMATRIX)]),
        STDMETHOD(POINTER(D3DXMATRIX), 'GetBoneOffsetMatrix', [DWORD]),
        STDMETHOD(HRESULT, 'Clone', [POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'Remap', [DWORD, POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'SetFVF', [DWORD]),
        STDMETHOD(HRESULT, 'SetDeclaration', [POINTER(D3DVERTEXELEMENT9)]),
        STDMETHOD(DWORD, 'GetFVF'),
        STDMETHOD(HRESULT, 'GetDeclaration', [POINTER(D3DVERTEXELEMENT9)]),
        STDMETHOD(HRESULT, 'UpdateSkinnedMesh', [POINTER(D3DXMATRIX), POINTER(D3DXMATRIX), POINTER(None), POINTER(None)]),
        STDMETHOD(HRESULT, 'ConvertToBlendedMesh', [POINTER(ID3DXMesh), DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXBuffer)), POINTER(DWORD), POINTER(DWORD), 
            POINTER(POINTER(ID3DXBuffer)), POINTER(POINTER(ID3DXMesh))]),
        STDMETHOD(HRESULT, 'ConvertToIndexedBlendedMesh', [POINTER(ID3DXMesh), DWORD, DWORD, POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXBuffer)), 
            POINTER(DWORD), POINTER(DWORD), POINTER(POINTER(ID3DXBuffer)), POINTER(POINTER(ID3DXMesh))]),
    ]
    
class ID3DXPatchMesh(IUnknown):
    _iid_ = GUID("{3CE6CC22-DBF2-44f4-894D-F9C34A337139}")
    _methods_ = [
        STDMETHOD(DWORD, 'GetNumPatches'),
        STDMETHOD(DWORD, 'GetNumVertices'),
        STDMETHOD(HRESULT, 'GetDeclaration', [POINTER(D3DVERTEXELEMENT9)]),
        STDMETHOD(DWORD, 'GetControlVerticesPerPatch'),
        STDMETHOD(DWORD, 'GetOptions'),
        STDMETHOD(HRESULT, 'GetDevice', [POINTER(POINTER(IDirect3DDevice9))]),
        STDMETHOD(HRESULT, 'GetPatchInfo', [POINTER(D3DXPATCHINFO)]),
        STDMETHOD(HRESULT, 'GetVertexBuffer', [POINTER(POINTER(IDirect3DVertexBuffer9))]),
        STDMETHOD(HRESULT, 'GetIndexBuffer', [POINTER(POINTER(IDirect3DIndexBuffer9))]),
        STDMETHOD(HRESULT, 'LockVertexBuffer', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'UnlockVertexBuffer'),
        STDMETHOD(HRESULT, 'LockIndexBuffer', [DWORD, POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'UnlockIndexBuffer'),
        STDMETHOD(HRESULT, 'LockAttributeBuffer', [DWORD, POINTER(POINTER(DWORD))]),
        STDMETHOD(HRESULT, 'UnlockAttributeBuffer'),
        STDMETHOD(HRESULT, 'GetTessSize', [c_float, DWORD, POINTER(DWORD), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'GenerateAdjacency', [c_float]),
        STDMETHOD(HRESULT, 'CloneMesh', [DWORD, POINTER(D3DVERTEXELEMENT9), POINTER(POINTER(None))]),
        STDMETHOD(HRESULT, 'Optimize', [DWORD]),
        STDMETHOD(HRESULT, 'SetDisplaceParam', [POINTER(IDirect3DBaseTexture9), DWORD, DWORD, DWORD, DWORD, DWORD]),
        STDMETHOD(HRESULT, 'GetDisplaceParam', [POINTER(POINTER(IDirect3DBaseTexture9)), POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(DWORD), POINTER(DWORD)]),
        STDMETHOD(HRESULT, 'Tessellate', [c_float, POINTER(ID3DXMesh)]),
        STDMETHOD(HRESULT, 'TessellateAdaptive', [POINTER(D3DXVECTOR4), DWORD, DWORD, POINTER(ID3DXMesh)]),
    ]
   