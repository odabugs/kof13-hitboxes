from ctypes import *
from ctypes.wintypes import *
from pydbg import *
from pydbg.defines import *

BYTE      = c_ubyte
WORD      = c_ushort
DWORD     = c_ulong
LPBYTE    = POINTER(c_ubyte)
LPTSTR    = POINTER(c_char) 
HANDLE    = c_void_p
PVOID     = c_void_p
LPVOID    = c_void_p
UINT_PTR  = c_ulong
SIZE_T    = c_ulong


class MARGINS(Structure):
	_fields_ = [
	("cxLeftWidth",    c_int),
	("cxRightWidth",   c_int),
	("cyTopHeight",    c_int),
	("cyBottomHeight", c_int) ]


WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)


class WNDCLASS(Structure):
	_fields_ = [
	("style",         c_uint),
	("lpfnWndProc",   WNDPROC),
	("cbClsExtra",    c_int),
	("cbWndExtra",    c_int),
	("hInstance",     c_int),
	("hIcon",         c_int),
	("hCursor",       c_int),
	("hbrBackground", c_int),
	("lpszMenuName",  c_char_p),
	("lpszClassName", c_char_p) ]


class SECURITY_ATTRIBUTES(Structure):
	_fields_ = [
	("Length",        c_ulong),
	("SecDescriptor", LPVOID),
	("InheritHandle", BOOL) ]


# Offsets that represent not-yet-understood values are named:
# Off_XXh, where XXh is the value's offset in hex.
# Byte "gaps" that represent parts of the struct not yet "explored"
# are named: Gap1, Gap2, etc., and are marked as byte arrays for padding.
class PLAYER(Structure):
	_fields_ = [
	("Gap1",     BYTE * 0x1C),
	("Off_1Ch",  c_int32), # signed or unsigned?
	("Gap2",     BYTE * 0x18),
	("Off_38h",  c_int32), # signed or unsigned?
	("Gap3",     BYTE * 0x14),
	("Health",   c_int32), # player HP
	("Gap4",     BYTE * 0x04),
	("Off_58h",  c_int32), # actual size???
	("Gap5",     BYTE * 0x0C),
	("Off_68h",  c_float),
	("Guard",    c_float), # guard crush meter
	("Off_70h",  c_float),
	("Gap6",     BYTE * 0x04),
	("Off_78h",  c_float),
	("Off_7Ch",  c_int32), # actual type/size???
	("Gap7",     BYTE * 0x14),
	("Stun",     c_float), # dizzy meter
	("Gap8",     BYTE * 0x14),
	("Combo",    c_int32), # combo hit counter
	("Tally",    c_int32), # running tally of hits landed
	("Gap9",     BYTE * 0x14),
	("Drive",    c_float), # drive meter
	("Gap10",    BYTE * 0x18),
	("XPivot",   c_float), # pivot X position?
	("YPivot",   c_float), # pivot Y position?
	("ZPivot",   c_float), # unused pivot coordinate?  always 0.0?
	("Gap11",    BYTE * 0x2C),
	("Super",    c_float), # super meter
	("Gap12",    BYTE * 0x04),
	("Off_124h", c_int32), # actual type???
	("Gap13",    BYTE * 0x24),
	("Off_14Ch", c_int32), # actual type???
	("Gap14",    BYTE * 0x54),
	("Facing",   c_byte), # left/right facing
	("Gap15",    BYTE * 0x07),
	("Off_1ACh", c_byte),
	]


class GAME_CAMERA(Structure):
	_fields_ = [
	("Gap1",    BYTE * 0x13C),
	("XShake",  c_float), # offset used on players when camera shakes
	("YShake",  c_float), # offset used on players when camera shakes
	("Gap2",    BYTE * 0x38),
	("XScroll", c_float), # camera X scroll offset (initially 0)
	("YScroll", c_float), # camera Y scroll offset (initially 0)
	]


# hitbox type handled by code block at 0050DC23h-0050DC69h
# hitboxes are stored in linked lists that end when the last element
# of the list points back to the first (see the "Next1" field)
class HITBOX1(Structure):
	pass

HITBOX1._fields_ = [
	("Next1",   c_uint32), # +00h: pointer to next HITBOX1
	("Next2",   c_uint32), # +04h: seems to usually match the value of Next1?
	# "Outer" seems to point to another structure of at least 6Ch bytes in size,
	# judging by code at 0050DCA0h-0050DCCAh
	("Outer",   c_uint32), # +08h: used by function starting at 0050DCA0h
	("Left",    c_float), # +0Ch: X origin of hitbox (left side)
	("Bottom",  c_float), # +10h: Y origin of hitbox (bottom side)
	("Width",   c_float), # +14h: 
	("Height",  c_float), # +18h: 
	("Flags",   c_uint32), # +1Ch: 
	# there may be some later fields missing here
	]


# hitbox type handled by code block at 0050EC9Ch-0050ECE2h
class HITBOX2(Structure):
	pass

HITBOX2._fields_ = [
	("Next1",   c_uint32), # pointer to next HITBOX2
	("Left",    c_float),
	("Bottom",  c_float),
	("Width",   c_float),
	("Height",  c_float),
	]
