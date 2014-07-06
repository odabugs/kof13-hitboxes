from ctypes import *
from ctypes.wintypes import *

BYTE      = c_uint8
WORD      = c_uint16
DWORD     = c_uint32
DWORDLONG = c_uint64
LPBYTE    = POINTER(c_ubyte)
LPTSTR    = POINTER(c_char) 
HANDLE    = c_void_p
PVOID     = c_void_p
LPVOID    = c_void_p
UINT_PTR  = c_ulong
SIZE_T    = c_ulong


WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)


# based on vertex format D3DFVF_XYZRHW | D3DFVF_DIFFUSE
class CUSTOMVERTEX(Structure):
	_fields_ = [
		("x",     c_float),
		("y",     c_float),
		("z",     c_float),
		("rhw",   c_float),
		("color", DWORD),
	]


class MARGINS(Structure):
	_fields_ = [
		("cxLeftWidth",    c_int),
		("cxRightWidth",   c_int),
		("cyTopHeight",    c_int),
		("cyBottomHeight", c_int),
	]


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
		("lpszClassName", c_char_p),
	]


class SECURITY_ATTRIBUTES(Structure):
	_fields_ = [
		("Length",        c_ulong),
		("SecDescriptor", LPVOID),
		("InheritHandle", BOOL),
	]


# Offsets that represent not-yet-understood values are named:
# Off_XXh, where XXh is the value's offset in hex.
# Byte "gaps" that represent parts of the struct not yet "explored"
# are named: Gap1, Gap2, etc., and are marked as byte arrays for padding.
class PLAYER(Structure):
	_fields_ = [
		("Gap1",     BYTE * 0x1C), # +00h through +1Ch
		("Off_1Ch",  c_int32), # +1Ch: signed or unsigned?
		("Gap2",     BYTE * 0x18), # +20h through +38h
		("Off_38h",  c_int32), # +38h: signed or unsigned?
		("Gap3",     BYTE * 0x14), # +3Ch through +50h
		("Health",   c_int32), # +50h: player HP
		("Gap4",     BYTE * 0x04), # +54h through +58h
		("Off_58h",  c_int32), # +58h: actual size???
		("Gap5",     BYTE * 0x0C), # +5Ch through +68h
		("Off_68h",  c_float), # +68h
		("Guard",    c_float), # +6Ch: guard crush meter
		("Off_70h",  c_float), # +70h
		("Gap6",     BYTE * 0x04), # +74h through +78h
		("Off_78h",  c_float), # +78h
		("Off_7Ch",  c_int32), # +7Ch: actual type/size???
		("Gap7",     BYTE * 0x14), # +80h through +94h
		("Stun",     c_float), # +94h: dizzy meter
		("Gap8",     BYTE * 0x14), #+98h through +ACh
		("Combo",    c_int32), # +ACh: combo hit counter
		("Tally",    c_int32), # +B0h: running tally of hits landed
		("Gap9",     BYTE * 0x14), # +B4h through C8h
		("Drive",    c_float), # +C8h: drive meter
		("Gap10",    BYTE * 0x18), # +CCh through +E4h
		("XPivot",   c_float), # +E4h: pivot X position?
		("YPivot",   c_float), # +E8h: pivot Y position?
		("ZPivot",   c_float), # +ECh: unused pivot coordinate?  always 0.0?
		("Gap11",    BYTE * 0x2C), # +F0h through +11Ch
		("Super",    c_float), # +11Ch: super meter
		("Gap12",    BYTE * 0x04), # + 120h through +124h
		("Off_124h", c_int32), # +124h: actual type???
		("Gap13",    BYTE * 0x24), # +128h through +14Ch
		("Off_14Ch", c_int32), # +14Ch: actual type???
		("Gap14",    BYTE * 0x54), # +150h through +1A4h
		("Facing",   c_byte), # +1A4h: left/right facing
		("Gap15",    BYTE * 0x08), # +1A4h through +1AC
		("Off_1ACh", c_byte), # +1ACh
	]


# player 1's PLAYER_TEAM starts at 00831DF4h in memory;
# player 2's starts at 00831FEF8h
class PLAYER_TEAM(Structure):
	_fields_ = [
		("Current",     c_uint32), # +00h; ID character currently in use
		("Gap1",        BYTE * 0x24), # +04h through +28h
		("First",       c_uint32), # +28h; ID of player's 1st character
		("FirstColor",  c_uint32), # +2Ch; 1st character's color choice
		("Gap2",        BYTE * 0x14), # +30h through +44h
		("Second",      c_uint32), # +44h; ID of player's 2nd character
		("SecondColor", c_uint32), # +48h; 2nd character's color choice
		("Gap3",        BYTE * 0x14), # +4Ch through +60h
		("Third",       c_uint32), # +60h; ID of player's 3rd character
		("ThirdColor",  c_uint32), # +64h; 3rd character's color choice
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
	("Next2",   c_uint32), # +04h: usually matches value of Next1?
	# "Outer" seems to point to another structure of at least 6Ch bytes,
	# judging by code at 0050DCA0h-0050DCCAh
	("Outer",   c_uint32), # +08h: used by function starting at 0050DCA0h
	("Left",    c_float), # +0Ch: X origin of hitbox (left side)
	("Bottom",  c_float), # +10h: Y origin of hitbox (bottom side)
	("Width",   c_float), # +14h: 
	("Height",  c_float), # +18h: 
	("Gap1",    BYTE*4),  # +1C through 1F
	("BoxID",   c_uint8), # +20h: 
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
	("Gap1",    BYTE * 4),
	("BoxID",   c_uint8), # 
]


# player 1's HITBOX_SET starts at 007EAC08h in memory;
# player 2's starts at 007EAC44h
# when reading pointers to pointers to HITBOX2, offset the second pointer by +8
class HITBOX_SET(Structure):
	_fields_ = [
		("Collision",       c_uint32), # +00h: pointer to pointer to HITBOX2
		("CollisionCount",  c_uint32), # +04h: 
		("Gap1",            BYTE * 4), # +08h through +0Ch
		("Attack",          c_uint32), # +0Ch: pointer to pointer to HITBOX1
		("AttackCount",     c_uint32), # +10h: 
		("Gap2",            BYTE * 4), # +14h through +18h
		("Armor",           c_uint32), # +18h: pointer to pointer to HITBOX1
		("ArmorCount",      c_uint32), # +1Ch: 
		("Gap3",            BYTE * 4), # +20h through +24h
		("Vulnerable",      c_uint32), # +24h: pointer to pointer to HITBOX1
		("VulnerableCount", c_uint32), # +28h: 
		("Gap4",            BYTE * 4), # +2Ch through +30h
		# Proximity is used by moves such as Kyo hcb+K
		("Proximity",       c_uint32), # +30h: pointer to pointer to HITBOX2
		("ProximityCount",  c_uint32), # +34h: 
	]
