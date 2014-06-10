
from ctypes import *
from ctypes.wintypes import *
from comtypes import * 

#********************************************************************
#
#   Typedefs and constants
#
#********************************************************************

REFGUID = POINTER(GUID)   

UINT = c_uint
INT = c_int

#Use Debug interfaces (requires that the SDK is installed).
D3DDEBUGENABLED = False 

DIRECT3D_VERSION = 0x0900
if D3DDEBUGENABLED:
    D3D_SDK_VERSION  = 32 | 0x80000000
else:
    D3D_SDK_VERSION  = 32

D3DX_DEFAULT = UINT(-1)

class D3DSHADE:
    FLAT               = 1
    GOURAUD            = 2
    PHONG              = 3

class D3DFILL:
    POINT               = 1
    WIREFRAME           = 2
    SOLID               = 3
    
class D3DBLEND:
    ZERO               = 1
    ONE                = 2
    SRCCOLOR           = 3
    INVSRCCOLOR        = 4
    SRCALPHA           = 5
    INVSRCALPHA        = 6
    DESTALPHA          = 7
    INVDESTALPHA       = 8
    DESTCOLOR          = 9
    INVDESTCOLOR       = 10
    SRCALPHASAT        = 11
    BOTHSRCALPHA       = 12
    BOTHINVSRCALPHA    = 13
    BLENDFACTOR        = 14
    INVBLENDFACTOR     = 15
    
class D3DBLENDOP:
    ADD              = 1
    SUBTRACT         = 2
    REVSUBTRACT      = 3
    MIN              = 4
    MAX              = 5
    
class D3DTADDRESS:
    WRAP            = 1
    MIRROR          = 2
    CLAMP           = 3
    BORDER          = 4
    MIRRORONCE      = 5

class D3DCULL:
    NONE                = 1
    CW                  = 2
    CCW                 = 3
    
class D3DCMP:
    NEVER                = 1
    LESS                 = 2
    EQUAL                = 3
    LESSEQUAL            = 4
    GREATER              = 5
    NOTEQUAL             = 6
    GREATEREQUAL         = 7
    ALWAYS               = 8
    
class D3DSTENCILOP:
    KEEP           = 1
    ZERO           = 2
    REPLACE        = 3
    INCRSAT        = 4
    DECRSAT        = 5
    INVERT         = 6
    INCR           = 7
    DECR           = 8
    
class D3DFOG:
    NONE                 = 0
    EXP                  = 1
    EXP2                 = 2
    LINEAR               = 3
    
class D3DZB:
    FALSE                 = 0
    TRUE                  = 1
    USEW                  = 2
    
class D3DPT:
    POINTLIST             = 1
    LINELIST              = 2
    LINESTRIP             = 3
    TRIANGLELIST          = 4
    TRIANGLESTRIP         = 5
    TRIANGLEFAN           = 6
    
class D3DTS:
    VIEW          = 2
    PROJECTION    = 3
    TEXTURE0      = 16
    TEXTURE1      = 17
    TEXTURE2      = 18
    TEXTURE3      = 19
    TEXTURE4      = 20
    TEXTURE5      = 21
    TEXTURE6      = 22
    TEXTURE7      = 23
    WORLD = 256 + 0
    
    
class D3DRS:
    ZENABLE                   = 7
    FILLMODE                  = 8
    SHADEMODE                 = 9
    ZWRITEENABLE              = 14
    ALPHATESTENABLE           = 15
    LASTPIXEL                 = 16
    SRCBLEND                  = 19
    DESTBLEND                 = 20
    CULLMODE                  = 22
    ZFUNC                     = 23
    ALPHAREF                  = 24
    ALPHAFUNC                 = 25
    DITHERENABLE              = 26
    ALPHABLENDENABLE          = 27
    FOGENABLE                 = 28
    SPECULARENABLE            = 29
    FOGCOLOR                  = 34
    FOGTABLEMODE              = 35
    FOGSTART                  = 36
    FOGEND                    = 37
    FOGDENSITY                = 38
    RANGEFOGENABLE            = 48
    STENCILENABLE             = 52
    STENCILFAIL               = 53
    STENCILZFAIL              = 54
    STENCILPASS               = 55
    STENCILFUNC               = 56
    STENCILREF                = 57 
    STENCILMASK               = 58
    STENCILWRITEMASK          = 59
    TEXTUREFACTOR             = 60
    WRAP0                     = 128
    WRAP1                     = 129
    WRAP2                     = 130
    WRAP3                     = 131
    WRAP4                     = 132
    WRAP5                     = 133
    WRAP6                     = 134
    WRAP7                     = 135
    CLIPPING                  = 136
    LIGHTING                  = 137
    AMBIENT                   = 139
    FOGVERTEXMODE             = 140
    COLORVERTEX               = 141
    LOCALVIEWER               = 142
    NORMALIZENORMALS          = 143
    DIFFUSEMATERIALSOURCE     = 145
    SPECULARMATERIALSOURCE    = 146
    AMBIENTMATERIALSOURCE     = 147
    EMISSIVEMATERIALSOURCE    = 148
    VERTEXBLEND               = 151
    CLIPPLANEENABLE           = 152
    POINTSIZE                 = 154
    POINTSIZE_MIN             = 155
    POINTSPRITEENABLE         = 156
    POINTSCALEENABLE          = 157
    POINTSCALE_A              = 158
    POINTSCALE_B              = 159
    POINTSCALE_C              = 160
    MULTISAMPLEANTIALIAS      = 161
    MULTISAMPLEMASK           = 162
    PATCHEDGESTYLE            = 163
    DEBUGMONITORTOKEN         = 165
    POINTSIZE_MAX             = 166
    INDEXEDVERTEXBLENDENABLE  = 167
    COLORWRITEENABLE          = 168
    TWEENFACTOR               = 170
    BLENDOP                   = 171
    POSITIONDEGREE            = 172
    NORMALDEGREE              = 173
    SCISSORTESTENABLE         = 174
    SLOPESCALEDEPTHBIAS       = 175
    ANTIALIASEDLINEENABLE     = 176
    MINTESSELLATIONLEVEL      = 178
    MAXTESSELLATIONLEVEL      = 179
    ADAPTIVETESS_X            = 180
    ADAPTIVETESS_Y            = 181
    ADAPTIVETESS_Z            = 182
    ADAPTIVETESS_W            = 183
    ENABLEADAPTIVETESSELLATION = 184
    TWOSIDEDSTENCILMODE       = 185
    CCW_STENCILFAIL           = 186
    CCW_STENCILZFAIL          = 187
    CCW_STENCILPASS           = 188
    CCW_STENCILFUNC           = 189
    COLORWRITEENABLE1         = 190
    COLORWRITEENABLE2         = 191
    COLORWRITEENABLE3         = 192
    BLENDFACTOR               = 193
    SRGBWRITEENABLE           = 194
    DEPTHBIAS                 = 195
    WRAP8                     = 198
    WRAP9                     = 199
    WRAP10                    = 200
    WRAP11                    = 201
    WRAP12                    = 202
    WRAP13                    = 203
    WRAP14                    = 204
    WRAP15                    = 205
    SEPARATEALPHABLENDENABLE  = 206
    SRCBLENDALPHA             = 207
    DESTBLENDALPHA            = 208
    BLENDOPALPHA              = 209
    
class D3DMCS:
    MATERIAL         = 0
    COLOR1           = 1
    COLOR2           = 2
    
class D3DTA:
    SELECTMASK     = 0x0000000f  # mask for arg selector
    DIFFUSE        = 0x00000000  # select diffuse color (read only)
    CURRENT        = 0x00000001  # select stage destination register (read/write)
    TEXTURE        = 0x00000002  # select texture color (read only)
    TFACTOR        = 0x00000003  # select D3DRS_TEXTUREFACTOR (read only)
    SPECULAR       = 0x00000004  # select specular color (read only)
    TEMP           = 0x00000005  # select temporary register color (read/write)
    CONSTANT       = 0x00000006  # select texture stage constant
    COMPLEMENT     = 0x00000010  # take 1.0 - x (read modifier)
    ALPHAREPLICATE = 0x00000020  # replicate alpha to color components (read modifier)
    
class D3DTSS:

    class TCI:
        PASSTHRU                            = 0x00000000
        CAMERASPACENORMAL                   = 0x00010000
        CAMERASPACEPOSITION                 = 0x00020000
        CAMERASPACEREFLECTIONVECTOR         = 0x00030000
        SPHEREMAP                           = 0x00040000
  
    COLOROP        =  1
    COLORARG1      =  2
    COLORARG2      =  3
    ALPHAOP        =  4
    ALPHAARG1      =  5
    ALPHAARG2      =  6
    BUMPENVMAT00   =  7
    BUMPENVMAT01   =  8
    BUMPENVMAT10   =  9
    BUMPENVMAT11   = 10
    TEXCOORDINDEX  = 11
    BUMPENVLSCALE  = 22
    BUMPENVLOFFSET = 23
    TEXTURETRANSFORMFLAGS = 24
    COLORARG0      = 26
    ALPHAARG0      = 27
    RESULTARG      = 28
    CONSTANT       = 32
    
class D3DSAMP:
    ADDRESSU       = 1
    ADDRESSV       = 2
    ADDRESSW       = 3
    BORDERCOLOR    = 4
    MAGFILTER      = 5
    MINFILTER      = 6
    MIPFILTER      = 7
    MIPMAPLODBIAS  = 8
    MAXMIPLEVEL    = 9
    MAXANISOTROPY  = 10
    SRGBTEXTURE    = 11
    ELEMENTINDEX   = 12
    DMAPOFFSET     = 13
    
class D3DTOP:
    DISABLE              = 1
    SELECTARG1           = 2
    SELECTARG2           = 3
    MODULATE             = 4
    MODULATE2X           = 5
    MODULATE4X           = 6
    ADD                  =  7
    ADDSIGNED            =  8
    ADDSIGNED2X          =  9
    SUBTRACT             = 10
    ADDSMOOTH            = 11
    BLENDDIFFUSEALPHA    = 12
    BLENDTEXTUREALPHA    = 13
    BLENDFACTORALPHA     = 14
    BLENDTEXTUREALPHAPM  = 15
    BLENDCURRENTALPHA    = 16
    PREMODULATE            = 17
    MODULATEALPHA_ADDCOLOR = 18                                  
    MODULATECOLOR_ADDALPHA = 19
    MODULATEINVALPHA_ADDCOLOR = 20
    MODULATEINVCOLOR_ADDALPHA = 21
    BUMPENVMAP           = 22
    BUMPENVMAPLUMINANCE  = 23
    DOTPRODUCT3          = 24
    MULTIPLYADD          = 25
    LERP                 = 26
    
class D3DTEXTUREFILTERTYPE:
    NONE            = 0
    POINT           = 1
    LINEAR          = 2
    ANISOTROPIC     = 3
    PYRAMIDALQUAD   = 6
    GAUSSIANQUAD    = 7
    
class D3DFVF:
    RESERVED0       = 0x001
    POSITION_MASK   = 0x400E
    XYZ             = 0x002
    XYZRHW          = 0x004
    XYZB1           = 0x006
    XYZB2           = 0x008
    XYZB3           = 0x00a
    XYZB4           = 0x00c
    XYZB5           = 0x00e
    XYZW            = 0x4002
    NORMAL          = 0x010
    PSIZE           = 0x020
    DIFFUSE         = 0x040
    SPECULAR        = 0x080
    TEXCOUNT_MASK   = 0xf00
    TEXCOUNT_SHIFT  = 8
    TEX0            = 0x000
    TEX1            = 0x100
    TEX2            = 0x200
    TEX3            = 0x300
    TEX4            = 0x400
    TEX5            = 0x500
    TEX6            = 0x600
    TEX7            = 0x700
    TEX8            = 0x800
    LASTBETA_UBYTE4 =  0x1000
    LASTBETA_D3DCOLOR = 0x8000
    RESERVED2        = 0x6000  
    
class D3DDECLUSAGE:
    POSITION = 0,
    BLENDWEIGHT =  1
    BLENDINDICES = 2
    NORMAL = 3
    PSIZE = 4
    TEXCOORD = 5
    TANGENT = 6
    BINORMAL = 7
    TESSFACTOR = 8
    POSITIONT = 9
    COLOR = 10
    FOG = 11
    DEPTH = 12
    SAMPLE = 13
    
class D3DDECLMETHOD:
    DEFAULT = 0
    PARTIALU = 1
    PARTIALV = 2
    CROSSUV = 3
    UV = 4
    LOOKUP = 5
    LOOKUPPRESAMPLED = 6
    
class D3DDECLTYPE:
    FLOAT1    =  0
    FLOAT2    =  1
    FLOAT3    =  2
    FLOAT4    =  3
    D3DCOLOR  =  4               
    UBYTE4    =  5
    SHORT2    =  6
    SHORT4    =  7
    UBYTE4N   =  8
    SHORT2N   =  9
    SHORT4N   = 10
    USHORT2N  = 11
    USHORT4N  = 12
    UDEC3     = 13
    DEC3N     = 14
    FLOAT16_2 = 15
    FLOAT16_4 = 16
    UNUSED    = 17
  
class D3DSWAPEFFECT:
    DISCARD           = 1
    FLIP              = 2
    COPY              = 3
    
class D3DPOOL:
    DEFAULT                 = 0
    MANAGED                 = 1
    SYSTEMMEM               = 2
    SCRATCH                 = 3
    
class D3DUSAGE:
    RENDERTARGET      = (0x00000001L)
    DEPTHSTENCIL      = (0x00000002L)
    DYNAMIC           = (0x00000200L)

    AUTOGENMIPMAP     = (0x00000400L)
    DMAP              = (0x00004000L)

    QUERY_LEGACYBUMPMAP           = (0x00008000L)
    QUERY_SRGBREAD                = (0x00010000L)
    QUERY_FILTER                  = (0x00020000L)
    QUERY_SRGBWRITE               = (0x00040000L)
    QUERY_POSTPIXELSHADER_BLENDING = (0x00080000L)
    QUERY_VERTEXTEXTURE           = (0x00100000L)
    QUERY_WRAPANDMIP	          =  (0x00200000L)

    WRITEONLY          = (0x00000008L)
    SOFTWAREPROCESSING = (0x00000010L)
    DONOTCLIP          = (0x00000020L)
    POINTS             = (0x00000040L)
    RTPATCHES          = (0x00000080L)
    NPATCHES           = (0x00000100L)
    
class D3DRTYPE:
    SURFACE                =  1
    VOLUME                 =  2
    TEXTURE                =  3
    VOLUMETEXTURE          =  4
    CUBETEXTURE            =  5
    VERTEXBUFFER           =  6
    INDEXBUFFER            =  7
    
class D3DCUBEMAP_FACES:
    FACE_POSITIVE_X     = 0
    FACE_NEGATIVE_X     = 1
    FACE_POSITIVE_Y     = 2
    FACE_NEGATIVE_Y     = 3
    FACE_POSITIVE_Z     = 4
    FACE_NEGATIVE_Z     = 5
    
class D3DLOCK:
    READONLY          = 0x00000010L
    DISCARD           = 0x00002000L
    NOOVERWRITE       = 0x00001000L
    NOSYSLOCK         = 0x00000800L
    DONOTWAIT         = 0x00004000L                  
    NO_DIRTY_UPDATE   = 0x00008000L
    
    
class D3DQUERYTYPE:
    VCACHE                 = 4
    RESOURCEMANAGER        = 5
    VERTEXSTATS            = 6
    EVENT                  = 8
    OCCLUSION              = 9
    TIMESTAMP              = 10
    TIMESTAMPDISJOINT      = 11
    TIMESTAMPFREQ          = 12
    PIPELINETIMINGS        = 13
    INTERFACETIMINGS       = 14
    VERTEXTIMINGS          = 15
    PIXELTIMINGS           = 16
    BANDWIDTHTIMINGS       = 17
    CACHEUTILIZATION       = 18
    
D3DISSUE_END = (1 << 0) 
D3DISSUE_BEGIN = (1 << 1) 
D3DGETDATA_FLUSH = (1 << 0) 
    
class D3DCLEAR:
    TARGET           = 0x00000001l 
    ZBUFFER          = 0x00000002l 
    STENCIL          = 0x00000004l  
    
class D3DDEVTYPE:
    HAL         = 1
    REF         = 2
    SW          = 3
    NULLREF     = 4
    
class D3DVERTEXBLENDFLAGS:
    DISABLE  = 0
    WEIGHTS1 = 1
    WEIGHTS2 = 2
    WEIGHTS3 = 3
    TWEENING = 255
    WEIGHTS0 = 256
    
class D3DTEXTURETRANSFORMFLAGS:
    DISABLE         = 0
    COUNT1          = 1
    COUNT2          = 2
    COUNT3          = 3
    COUNT4          = 4
    PROJECTED       = 256
    
def MAKEFOURCC(a, b, c, d):
    return ord(a) | (ord(b) << 8) | (ord(c) << 16) | (ord(d) << 24)
    
class D3DFORMAT:
    UNKNOWN              =  0
    R8G8B8               = 20
    A8R8G8B8             = 21
    X8R8G8B8             = 22
    R5G6B5               = 23
    X1R5G5B5             = 24
    A1R5G5B5             = 25
    A4R4G4B4             = 26
    R3G3B2               = 27
    A8                   = 28
    A8R3G3B2             = 29
    X4R4G4B4             = 30
    A2B10G10R10          = 31
    A8B8G8R8             = 32
    X8B8G8R8             = 33
    G16R16               = 34
    A2R10G10B10          = 35
    A16B16G16R16         = 36
    A8P8                 = 40
    P8                   = 41
    L8                   = 50
    A8L8                 = 51
    A4L4                 = 52
    V8U8                 = 60
    L6V5U5               = 61
    X8L8V8U8             = 62
    Q8W8V8U8             = 63
    V16U16               = 64
    A2W10V10U10          = 67
    UYVY                 = MAKEFOURCC('U', 'Y', 'V', 'Y')
    R8G8_B8G8            = MAKEFOURCC('R', 'G', 'B', 'G')
    YUY2                 = MAKEFOURCC('Y', 'U', 'Y', '2')
    G8R8_G8B8            = MAKEFOURCC('G', 'R', 'G', 'B')
    DXT1                 = MAKEFOURCC('D', 'X', 'T', '1')
    DXT2                 = MAKEFOURCC('D', 'X', 'T', '2')
    DXT3                 = MAKEFOURCC('D', 'X', 'T', '3')
    DXT4                 = MAKEFOURCC('D', 'X', 'T', '4')
    DXT5                 = MAKEFOURCC('D', 'X', 'T', '5')
    D16_LOCKABLE         = 70
    D32                  = 71
    D15S1                = 73
    D24S8                = 75
    D24X8                = 77
    D24X4S4              = 79
    D16                  = 80
    D32F_LOCKABLE        = 82
    D24FS8               = 83
    L16                  = 81
    VERTEXDATA           =100
    INDEX16              =101
    INDEX32              =102
    Q16W16V16U16         =110
    MULTI2_ARGB8         = MAKEFOURCC('M','E','T','1'),
    R16F                 = 111
    G16R16F              = 112
    A16B16G16R16F        = 113
    R32F                 = 114
    G32R32F              = 115
    A32B32G32R32F        = 116
    CxV8U8               = 117
    
class D3DCREATE:   
    FPU_PRESERVE                 = 0x00000002L
    MULTITHREADED                = 0x00000004L
    PUREDEVICE                   = 0x00000010L
    SOFTWARE_VERTEXPROCESSING    = 0x00000020L
    HARDWARE_VERTEXPROCESSING    = 0x00000040L
    MIXED_VERTEXPROCESSING       = 0x00000080L
    DISABLE_DRIVER_MANAGEMENT    = 0x00000100L
    ADAPTERGROUP_DEVICE          = 0x00000200L
    DISABLE_DRIVER_MANAGEMENT_EX = 0x00000400L
    NOWINDOWCHANGES				= 0x00000800L

class D3DPRESENT:        
    INTERVAL_DEFAULT    = 0x00000000L
    INTERVAL_ONE        = 0x00000001L
    INTERVAL_TWO        = 0x00000002L
    INTERVAL_THREE      = 0x00000004L
    INTERVAL_FOUR       = 0x00000008L
    INTERVAL_IMMEDIATE  = 0x80000000L
    
    DONOTWAIT                  = 0x00000001L
    LINEAR_CONTENT             = 0x00000002L
    
class D3DLIGHTTYPE:
    POINT          = 1
    SPOT           = 2
    DIRECTIONAL    = 3
    
#********************************************************************
#   D3DX constants
#********************************************************************
    
class D3DXFONT:
    TOP                     = 0x00000000
    LEFT                    = 0x00000000
    CENTER                  = 0x00000001
    RIGHT                   = 0x00000002
    VCENTER                 = 0x00000004
    BOTTOM                  = 0x00000008
    WORDBREAK               = 0x00000010
    SINGLELINE              = 0x00000020
    EXPANDTABS              = 0x00000040
    TABSTOP                 = 0x00000080
    NOCLIP                  = 0x00000100
    EXTERNALLEADING         = 0x00000200
    CALCRECT                = 0x00000400
    NOPREFIX                = 0x00000800
    INTERNAL                = 0x00001000
    
class D3DXSPRITE:
    DONOTSAVESTATE              = (1 << 0)
    DONOTMODIFY_RENDERSTATE     = (1 << 1)
    OBJECTSPACE                 = (1 << 2)
    BILLBOARD                   = (1 << 3)
    ALPHABLEND                  = (1 << 4)
    SORT_TEXTURE                = (1 << 5)
    SORT_DEPTH_FRONTTOBACK      = (1 << 6)
    SORT_DEPTH_BACKTOFRONT      = (1 << 7)
    
    
class D3DXMESH:
    BIT32                  = 0x001
    DONOTCLIP              = 0x002
    POINTS                 = 0x004 
    RTPATCHES              = 0x008
    NPATCHES               = 0x4000
    VB_SYSTEMMEM           = 0x010
    VB_MANAGED             = 0x020 
    VB_WRITEONLY           = 0x040
    VB_DYNAMIC             = 0x080
    VB_SOFTWAREPROCESSING = 0x8000
    IB_SYSTEMMEM           = 0x100
    IB_MANAGED             = 0x200
    IB_WRITEONLY           = 0x400
    IB_DYNAMIC             = 0x800
    IB_SOFTWAREPROCESSING = 0x10000
    VB_SHARE               = 0x1000
    USEHWONLY              = 0x2000
    SYSTEMMEM              = 0x110
    MANAGED                = 0x220
    WRITEONLY              = 0x440
    DYNAMIC                = 0x880
    SOFTWAREPROCESSING   = 0x18000
    
#********************************************************************
#   D3DX Structures
#********************************************************************
    
class D3DXFONT_DESCW(Structure):
    _fields_ = [
        ('Height', INT),
        ('Width', UINT),
        ('Weight', UINT),
        ('MipLevels', UINT),  
        ('Italic', BOOL),
        ('CharSet', BYTE),
        ('OutputPrecision', BYTE),
        ('Quality', BYTE),    
        ('PitchAndFamily', BYTE),  
        ('FaceName', WCHAR * 32),  
    ]

class TEXTMETRICW(Structure):
    _fields_ = [
        ('tmHeight', LONG),
        ('tmAscent', LONG),
        ('tmDescent', LONG),
        ('tmInternalLeading', LONG),  
        ('tmExternalLeading', LONG),
        ('tmAveCharWidth', LONG),
        ('tmMaxCharWidth', LONG),
        ('tmWeight', LONG),    
        ('tmOverhang', LONG),  
        ('tmDigitizedAspectX', LONG),
        ('tmDigitizedAspectY', LONG),
        ('tmFirstChar', WCHAR),
        ('tmLastChar', WCHAR),
        ('tmDefaultChar', WCHAR),  
        ('tmBreakChar', WCHAR),
        ('tmItalic', BYTE),
        ('tmUnderlined', BYTE),
        ('tmStruckOut', BYTE),    
        ('tmPitchAndFamily', BYTE),  
        ('tmCharSet', BYTE),
    ]
    
class D3DXVECTOR2(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
    ]
    
class D3DXVECTOR4(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('w', c_float),
    ]
    
class D3DXQUATERNION(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('w', c_float),
    ]
    
class D3DXEFFECT_DESC(Structure):
    _fields_ = [
        ('Creator', LPCSTR),
        ('Parameters', UINT),
        ('Techniques', UINT),
        ('Functions', UINT),      
    ]

class D3DXPARAMETER_DESC(Structure):
    _fields_ = [
        ('Name', LPCSTR),
        ('Semantic', LPCSTR),
        ('Class', DWORD),
        ('Type', DWORD),      
        ('Rows', UINT),  
        ('Columns', UINT), 
        ('Elements', UINT),   
        ('Annotations', UINT),  
        ('StructMembers', UINT), 
        ('Flags', DWORD),  
        ('Bytes', UINT),  
    ]
    
class D3DXTECHNIQUE_DESC(Structure):
    _fields_ = [
        ('Name', LPCSTR),
        ('Passes', UINT),
        ('Annotations', UINT),  
    ]
    
class D3DXPASS_DESC(Structure):
    _fields_ = [
        ('Name', LPCSTR),
        ('Annotations', UINT), 
        ('pVertexShaderFunction', POINTER(DWORD)), 
        ('pPixelShaderFunction', POINTER(DWORD)), 
    ]
    
class D3DXFUNCTION_DESC(Structure):
    _fields_ = [
        ('Name', LPCSTR),
        ('Annotations', UINT), 
    ]  
    
class D3DXATTRIBUTERANGE(Structure):
    _fields_ = [
        ('AttribId', DWORD),
        ('FaceStart', DWORD),
        ('FaceCount', DWORD),
        ('VertexStart', DWORD),  
        ('VertexCount', DWORD),
    ]
    
class D3DXATTRIBUTEWEIGHTS(Structure):
    _fields_ = [
        ('Position', c_float),
        ('Boundary', c_float),
        ('Normal', c_float),
        ('Diffuse', c_float),  
        ('Specular', c_float),
        ('Texcoord', c_float * 8),  
        ('Tangent', c_float), 
        ('Binormal', c_float), 
    ]

class D3DXPATCHINFO(Structure):
    _fields_ = [
        ('PatchType', DWORD),
        ('Degree', DWORD),
        ('Basis', DWORD),
    ]
    
#********************************************************************
#   D3D Structures
#********************************************************************

class PALETTEENTRY(Structure):
    _fields_ = [
        ('peRed', BYTE),
        ('peGreen', BYTE),
        ('peBlue', BYTE),
        ('peFlags', BYTE),
    ]

class RGNDATAHEADER(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('iType', DWORD),
        ('nCount', DWORD),
        ('nRgnSize', DWORD),
        ('rcBound', DWORD),
    ]

class RGNDATA(Structure):
    _fields_ = [
        ('rdh', RGNDATAHEADER),
        ('buffer', c_char * 1),
    ]

class D3DVECTOR(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
    ]

class D3DCOLORVALUE(Structure):
    _fields_ = [
        ('r', c_float),
        ('g', c_float),
        ('b', c_float),
        ('a', c_float),    
    ]

class D3DRECT(Structure):
    _fields_ = [
        ('x1', LONG),
        ('y1', LONG),
        ('x2', LONG),
        ('y2', LONG),    
    ]
    
class D3DMATRIX(Structure):
    _fields_ = [
        ('m', c_float * (4 * 4)),    
    ]
    
class D3DVIEWPORT9(Structure):
    _fields_ = [
        ('X', DWORD),
        ('Y', DWORD),
        ('Width', DWORD),
        ('Height', DWORD),    
        ('MinZ', c_float),      
        ('MaxZ', c_float),      
    ]
    
class D3DCLIPSTATUS9(Structure):
    _fields_ = [
        ('ClipUnion', DWORD),
        ('ClipIntersection', DWORD), 
    ]
    
class D3DMATERIAL9(Structure):
    _fields_ = [
        ('Diffuse', D3DCOLORVALUE),
        ('Ambient', D3DCOLORVALUE),
        ('Specular', D3DCOLORVALUE),
        ('Emissive', D3DCOLORVALUE),    
        ('Power', c_float),          
    ]
     
class D3DXMATERIAL(Structure):
    _fields_ = [
        ('MatD3D', D3DMATERIAL9),
        ('pTextureFilename', LPSTR), 
    ]  
     
class D3DLIGHT9(Structure):
    _fields_ = [
        ('Type', DWORD),
        ('Diffuse', D3DCOLORVALUE),
        ('Specular', D3DCOLORVALUE),
        ('Ambient', D3DCOLORVALUE),    
        ('Position', D3DVECTOR),   
        ('Direction', D3DVECTOR),  
        ('Range', c_float),  
        ('Falloff', c_float),  
        ('Attenuation0', c_float),   
        ('Attenuation1', c_float),  
        ('Attenuation2', c_float),  
        ('Theta', c_float),  
        ('Phi', c_float),   
    ]
    
class D3DVERTEXELEMENT9(Structure):
    _fields_ = [
        ('Stream', WORD),
        ('Offset', WORD),
        ('Type', BYTE),
        ('Method', BYTE),    
        ('Usage', BYTE),   
        ('UsageIndex', BYTE),    
    ]  
  
def D3DDECL_END():
    return D3DVERTEXELEMENT9(0xFF, 0, D3DDECLTYPE.UNUSED, 0, 0, 0)
  
class D3DDISPLAYMODE(Structure):
    _fields_ = [
        ('Width', UINT),
        ('Height', UINT),
        ('RefreshRate', UINT),
        ('Format', DWORD),     
    ]
  
class D3DDEVICE_CREATION_PARAMETERS(Structure):
    _fields_ = [
        ('AdapterOrdinal', UINT),
        ('DeviceType', DWORD),
        ('hFocusWindow', HWND),
        ('BehaviorFlags', DWORD),     
    ]
    
class D3DPRESENT_PARAMETERS(Structure):
    _fields_ = [
        ('BackBufferWidth', UINT),
        ('BackBufferHeight', UINT),
        ('BackBufferFormat', DWORD),
        ('BackBufferCount', UINT),              
        ('MultiSampleType', DWORD),
        ('MultiSampleQuality', DWORD),
        ('SwapEffect', DWORD),
        ('hDeviceWindow', HWND),
        ('Windowed', BOOL),              
        ('EnableAutoDepthStencil', BOOL),
        ('AutoDepthStencilFormat', DWORD), 
        ('Flags', DWORD),
        ('FullScreen_RefreshRateInHz', UINT),              
        ('PresentationInterval', UINT),
    ]
    
class D3DGAMMARAMP(Structure):
    _fields_ = [
        ('red', WORD * 256),
        ('green', WORD * 256),
        ('blue', WORD * 256),
    ]
    
class D3DVERTEXBUFFER_DESC(Structure):
    _fields_ = [
        ('Format', DWORD),
        ('Type', DWORD),
        ('Usage', DWORD),
        ('Pool', DWORD),
        ('Size', UINT),   
        ('FVF', DWORD), 
    ]  
    
class D3DINDEXBUFFER_DESC(Structure):
    _fields_ = [
        ('Format', DWORD),
        ('Type', DWORD),
        ('Usage', DWORD),
        ('Pool', DWORD),
        ('Size', UINT),   
    ]
    
    
class D3DSURFACE_DESC(Structure):
    _fields_ = [
        ('Format', DWORD),
        ('Type', DWORD),
        ('Usage', DWORD),
        ('Pool', DWORD),
        ('MultiSampleType', DWORD),   
        ('MultiSampleQuality', DWORD),  
        ('Width', UINT),  
        ('Height', UINT),       
    ]
    
class D3DVOLUME_DESC(Structure):
    _fields_ = [
        ('Format', DWORD),
        ('Type', DWORD),
        ('Usage', DWORD),
        ('Pool', DWORD),
        ('Width', UINT),  
        ('Height', UINT), 
        ('Depth', UINT),      
    ]
    
class D3DLOCKED_RECT(Structure):
    _fields_ = [
        ('Pitch', INT),
        ('pBits', c_void_p),    
    ]
    
class D3DBOX(Structure):
    _fields_ = [
        ('Left', UINT),
        ('Top', UINT),
        ('Right', UINT),
        ('Bottom', UINT),
        ('Front', UINT),  
        ('Back', UINT),    
    ]
    
class D3DLOCKED_BOX(Structure):
    _fields_ = [
        ('RowPitch', INT),
        ('SlicePitch', INT),
        ('pBits', c_void_p),   
    ]
    
class D3DRANGE(Structure):
    _fields_ = [
        ('Offset', UINT),
        ('Size', UINT),  
    ]
    
class D3DRECTPATCH_INFO(Structure):
    _fields_ = [
        ('StartVertexOffsetWidth', UINT),
        ('StartVertexOffsetHeight', UINT), 
        ('Width', UINT),
        ('Height', UINT), 
        ('Stride', UINT),
        ('Basis', DWORD), 
        ('Degree', DWORD),   
    ]
    
class D3DTRIPATCH_INFO(Structure):
    _fields_ = [
        ('StartVertexOffset', UINT),
        ('NumVertices', UINT), 
        ('Basis', DWORD),
        ('Degree', DWORD),  
    ]
    
MAX_DEVICE_IDENTIFIER_STRING = 512
    
class D3DADAPTER_IDENTIFIER9(Structure):
    _fields_ = [
        ('Driver', c_char * MAX_DEVICE_IDENTIFIER_STRING),
        ('Description', c_char * MAX_DEVICE_IDENTIFIER_STRING), 
        ('DeviceName', c_char * 32),
        ('DriverVersion', LARGE_INTEGER), 
        ('VendorId', DWORD),
        ('DeviceId', DWORD), 
        ('SubSysId', DWORD),   
        ('Revision', DWORD),   
        ('DeviceIdentifier', GUID),   
        ('WHQLLevel', DWORD),    
    ]
    
class D3DRASTER_STATUS(Structure):
    _fields_ = [
        ('InVBlank', BOOL),
        ('ScanLine', UINT), 
    ]
    
class D3DRESOURCESTATS(Structure):
    _fields_ = [
        ('bThrashing', UINT),
        ('ApproxBytesDownloaded', DWORD), 
        ('NumEvicts', DWORD),
        ('NumVidCreates', DWORD), 
        ('LastPri', DWORD),
        ('NumUsed', DWORD), 
        ('NumUsedInVidMem', DWORD),   
        ('WorkingSet', DWORD),   
        ('WorkingSetBytes', DWORD),   
        ('TotalManaged', DWORD), 
        ('TotalBytes', DWORD), 
    ]
    
class D3DDEVINFO_RESOURCEMANAGER(Structure):
    _fields_ = [
        ('stats', D3DRESOURCESTATS * (7+1)),
    ]
    
class D3DDEVINFO_D3DVERTEXSTATS(Structure):
    _fields_ = [
        ('NumRenderedTriangles', DWORD),
        ('NumExtraClippingTriangles', DWORD),    
    ]  
    
class D3DDEVINFO_VCACHE(Structure):
    _fields_ = [
        ('Pattern', DWORD),
        ('OptMethod', DWORD),    
        ('CacheSize', DWORD),
        ('MagicNumber', DWORD),       
    ]  
    
class D3DDEVINFO_D3D9PIPELINETIMINGS(Structure):
    _fields_ = [
        ('VertexProcessingTimePercent', c_float),
        ('PixelProcessingTimePercent', c_float),    
        ('OtherGPUProcessingTimePercent', c_float),
        ('GPUIdleTimePercent', c_float),       
    ]  
    
class D3DDEVINFO_D3D9INTERFACETIMINGS(Structure):
    _fields_ = [
        ('WaitingForGPUToUseApplicationResourceTimePercent', c_float),
        ('WaitingForGPUToAcceptMoreCommandsTimePercent', c_float),    
        ('WaitingForGPUToStayWithinLatencyTimePercent', c_float),
        ('WaitingForGPUExclusiveResourceTimePercent', c_float),  
        ('WaitingForGPUOtherTimePercent', c_float),       
    ]  
    
class D3DDEVINFO_D3D9STAGETIMINGS(Structure):
    _fields_ = [
        ('MemoryProcessingPercent', c_float),
        ('ComputationProcessingPercent', c_float),         
    ]  
    
class D3DDEVINFO_D3D9BANDWIDTHTIMINGS(Structure):
    _fields_ = [
        ('MaxBandwidthUtilized', c_float),
        ('FrontEndUploadMemoryUtilizedPercent', c_float),    
        ('VertexRateUtilizedPercent', c_float),
        ('TriangleSetupRateUtilizedPercent', c_float),  
        ('FillRateUtilizedPercent', c_float),       
    ]  
    
class D3DDEVINFO_D3D9CACHEUTILIZATION(Structure):
    _fields_ = [
        ('TextureCacheHitRate', c_float),
        ('PostTransformVertexCacheHitRate', c_float),         
    ]  
    
class D3DVSHADERCAPS2_0(Structure):
    _fields_ = [
        ('Caps', DWORD),  
        ('DynamicFlowControlDepth', INT),  
        ('NumTemps', INT),  
        ('StaticFlowControlDepth', INT),  
    ]
    
class D3DPSHADERCAPS2_0(Structure):
    _fields_ = [
        ('Caps', DWORD),  
        ('DynamicFlowControlDepth', INT),  
        ('NumTemps', INT),  
        ('StaticFlowControlDepth', INT),  
        ('NumInstructionSlots', INT),       
    ]
    
class D3DCAPS9(Structure):
    _fields_ = [
        ('DeviceType', DWORD),  
        ('AdapterOrdinal', UINT),  
        ('Caps', DWORD),  
        ('Caps2', DWORD),  
        ('Caps3', DWORD),  
        ('PresentationIntervals', DWORD),  
        ('CursorCaps', DWORD),  
        ('DevCaps', DWORD), 
        ('PrimitiveMiscCaps', DWORD),  
        ('RasterCaps', DWORD),  
        ('ZCmpCaps', DWORD),  
        ('SrcBlendCaps', DWORD),  
        ('DestBlendCaps', DWORD),  
        ('AlphaCmpCaps', DWORD),  
        ('ShadeCaps', DWORD),  
        ('TextureCaps', DWORD), 
        ('TextureFilterCaps', DWORD),  
        ('CubeTextureFilterCaps', DWORD),  
        ('VolumeTextureFilterCaps', DWORD),  
        ('TextureAddressCaps', DWORD),  
        ('VolumeTextureAddressCaps', DWORD),  
        ('LineCaps', DWORD),  
        ('MaxTextureWidth', DWORD),  
        ('MaxTextureHeight', DWORD), 
        ('MaxVolumeExtent', DWORD),  
        ('MaxTextureRepeat', DWORD),    
        ('MaxTextureAspectRatio', DWORD),  
        ('MaxAnisotropy', DWORD),     
        ('MaxVertexW', c_float),  
        ('GuardBandLeft', c_float),    
        ('GuardBandTop', c_float),  
        ('GuardBandRight', c_float), 
        ('GuardBandBottom', c_float),  
        ('ExtentsAdjust', c_float),    
        ('StencilCaps', DWORD),  
        ('FVFCaps', DWORD),     
        ('TextureOpCaps', DWORD),  
        ('MaxTextureBlendStages', DWORD), 
        ('MaxSimultaneousTextures', DWORD),  
        ('VertexProcessingCaps', DWORD), 
        ('MaxActiveLights', DWORD),  
        ('MaxUserClipPlanes', DWORD), 
        ('MaxVertexBlendMatrices', DWORD),  
        ('MaxVertexBlendMatrixIndex', DWORD), 
        ('MaxPointSize', c_float),  
        ('MaxPrimitiveCount', DWORD), 
        ('MaxVertexIndex', DWORD),  
        ('MaxStreams', DWORD), 
        ('MaxStreamStride', DWORD),  
        ('VertexShaderVersion', DWORD), 
        ('MaxVertexShaderConst', DWORD),  
        ('PixelShaderVersion', DWORD),
        ('PixelShader1xMaxValue', c_float), 
        ('DevCaps2', DWORD),  
        ('MaxNpatchTessellationLevel', c_float),
        ('Reserved5', DWORD), 
        ('MasterAdapterOrdinal', UINT),  
        ('AdapterOrdinalInGroup', UINT),
        ('NumberOfAdaptersInGroup', UINT), 
        ('DeclTypes', DWORD),  
        ('NumSimultaneousRTs', DWORD),
        ('StretchRectFilterCaps', DWORD),  
        ('VS20Caps', D3DVSHADERCAPS2_0),
        ('PS20Caps', D3DPSHADERCAPS2_0),  
        ('VertexTextureFilterCaps', DWORD),
        ('MaxVShaderInstructionsExecuted', DWORD),  
        ('MaxPShaderInstructionsExecuted', DWORD),
        ('MaxVertexShader30InstructionSlots', DWORD),  
        ('MaxPixelShader30InstructionSlots', DWORD),
    ] 

    