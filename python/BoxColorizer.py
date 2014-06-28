from Global import reverseDict
#from Colors import *
#from CStructures import HITBOX1, HITBOX2

# hitbox types
BOX_COLLISION = 0
BOX_VULNERABLE = 1
BOX_ATTACK = 2
BOX_THROW = 3
# vulnerable and attack hitboxes on projectiles
BOX_PROJ_VULN = 4
BOX_PROJ_ATTACK = 5
# blocking and moves with guard point
BOX_GUARD = 6
# for moves with proximity detection (e.g., Kyo hcb+K)
BOX_PROXIMITY = 7


# return colorizer function that always returns the same color,
# regardless of arguments passed (for "knowns" such as pushboxes)
def fixedColor(color):
	return (lambda character, boxID: color)


# for regular attacks, throws and projectile vulnerable/attack boxes
def attackColorizer(charID, boxID):
	boxType = specialBoxIDs[charID].get(boxID, BOX_ATTACK)
	return colorsByBoxType[boxType]


# this is temporary and will be replaced when config file
# support is fully implemented, hence it has obvious gaps
# (seriously; box color info doesn't belong here long term)
# (nor in Renderer for that matter...)
colorsByBoxType = {
	BOX_ATTACK      : 0xFF0000,
	BOX_THROW       : 0xFF00FF,
	BOX_PROJ_VULN   : 0xFFFF00,
	BOX_PROJ_ATTACK : 0xFF8000,
}


# ID numbers to character names
charNamesByID = {
	# ID : Character      ID : Character       ID : Character
	0x00 : "Elisabeth", 0x01 : "Duo Lon",    0x02 : "Shen",
	0x03 : "Kyo",       0x04 : "Benimaru",   0x05 : "Daimon",
	0x06 : "Iori",      0x07 : "Mature",     0x08 : "Vice",
	0x09 : "Terry",     0x0A : "Andy",       0x0B : "Joe",
	0x0C : "Athena",    0x0D : "Kensou",     0x0E : "Chin",
	0x0F : "Kim",       0x10 : "Hwa Jai",    0x11 : "Raiden",
	0x12 : "Ryo",       0x13 : "Robert",     0x14 : "Takuma",
	0x15 : "Ralf",      0x16 : "Clark",      0x17 : "Leona",
	0x18 : "Ash",     # 0x19 : Unused,       0x1A : Unused,
	0x1B : "Mai",       0x1C : "King",       0x1D : "Yuri",
	0x1E : "EX Iori",   0x1F : "Billy",      # spacer
	0x20 : "K\'",       0x21 : "Kula",       0x22 : "Maxima",
	0x23 : "EX Kyo",    0x24 : "Mr. Karate", 0x25 : "Saiki",
}
lowercase = lambda string: string.lower()
charIDsByName = reverseDict(charNamesByID, valFn=lowercase)
allCharIDs = charNamesByID.keys()
IDbyName = lambda charName: charIDsByName.get(charName.lower(), None)
nameByID = lambda charID: charNamesByID.get(charID, None)


# list per character of box IDs corresponding to projectile
# vulnerable, projectile attack, and throw hitboxes
# IDs 0x3F through 0x43 seem to always be projectile vulnerable hitboxes?
# BOX_PROJ_VULN IDs are used in so many places that it's not worth listing moves
specialBoxIDs = {
	# template (be sure to use IDbyName("Name") in place of -1)
	-1 : {
		0x00 : BOX_PROJ_VULN,   # 
		0x01 : BOX_THROW,       # 
		0x02 : BOX_PROJ_ATTACK, # 
	},
	IDbyName("Elisabeth") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x5C : BOX_PROJ_ATTACK, # qcf+A
		0x5D : BOX_PROJ_ATTACK, # qcf+C
		0x5E : BOX_PROJ_ATTACK, # qcf+AC
		0x6A : BOX_PROJ_ATTACK, # qcf,qcf+A
		0x6C : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x69 : BOX_THROW,       # hcb,f+A or C
		0x6F : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Duo Lon") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x64 : BOX_PROJ_ATTACK, # qcb+A or C
		0x65 : BOX_PROJ_ATTACK, # qcb+AC
		0x5C : BOX_THROW,       # C throw, D throw
		0x6E : BOX_THROW,       # hcb,hcb+AC
	},
	IDbyName("Shen") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		0x5B : BOX_THROW,       # hcb,f+A or C or AC (surprising that AC, which has a different hit effect, has the same number.)
		0x68 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Kyo") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x52 : BOX_THROW,       # C throw, D throw
		0x6F : BOX_THROW,       # hcb+BD
		0x71 : BOX_PROJ_ATTACK, # qcb,qcf+A or C (grounded)
		0x72 : BOX_PROJ_ATTACK, # qcb,qcf+A or C (midair)
		0x73 : BOX_PROJ_ATTACK, # qcb,qcf+AC (grounded)
		0x74 : BOX_PROJ_ATTACK, # qcb,qcf+AC (midair)
		0x75 : BOX_PROJ_ATTACK, # qcf+A or C
		0x77 : BOX_PROJ_ATTACK, # qcf+AC
		0x78 : BOX_PROJ_ATTACK, # qcf,qcf+AC (neomax)
	},
	IDbyName("Benimaru") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x4C : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x56 : BOX_PROJ_ATTACK, # qcf+C (grounded)
		0x57 : BOX_PROJ_ATTACK, # qcf+C (grounded) (2nd hit)
		0x58 : BOX_PROJ_ATTACK, # qcf+A (grounded)
		0x59 : BOX_PROJ_ATTACK, # qcf+A (midair)
		0x5A : BOX_PROJ_ATTACK, # qcf+C (midair)
		0x5B : BOX_PROJ_ATTACK, # qcf+A (grounded) (2nd hit)
		0x5C : BOX_PROJ_ATTACK, # qcf+AC (grounded)
		0x5E : BOX_PROJ_ATTACK, # qcf+AC (midair)
		0x6C : BOX_PROJ_ATTACK, # taunt
		0x6D : BOX_PROJ_ATTACK, # qcb+A or C
		0x6E : BOX_PROJ_ATTACK, # qcf,qcf+AC (hit)
		0x6F : BOX_PROJ_ATTACK, # qcf,qcf+A or C
		0x70 : BOX_PROJ_ATTACK, # qcf,qcf+A or C (last hit)
		0x71 : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x72 : BOX_PROJ_ATTACK, # qcf,qcf+AC (last hit)
		0x73 : BOX_PROJ_ATTACK, # qcb,qcb+A or C
		0x74 : BOX_PROJ_ATTACK, # qcb,qcb+A (on hit)
		0x75 : BOX_THROW,       # C throw, D throw
		0x77 : BOX_THROW,       # hcb,f+A or C
		0x78 : BOX_THROW,       # hcb,f+AC
		0x79 : BOX_PROJ_ATTACK, # qcf,qcf+BD (neomax)
		0x7A : BOX_PROJ_ATTACK, # qcf,qcf+BD (neomax) (last hit)
	},
	IDbyName("Daimon") : {
		0x5A : BOX_THROW,       # hcb,f+A or C
		0x5B : BOX_THROW,       # hcb,f+AC
		0x61 : BOX_THROW,       # hcb,hcb+A or C
		0x63 : BOX_THROW,       # hcb,hcb+AC
		0x63 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Iori") : {
		#0x1A : 				# This is the ID of the hurtbox on the startup of qcb+BD. Presumably it denotes projectile invincibility. Later on it becomes 0x11, which is the default.
		0x5D : BOX_THROW,       # hcf+A or C
		0x5E : BOX_THROW,       # hcf+AC
		0x6F : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Mature") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x5B : BOX_PROJ_ATTACK, # qcf,hcb+A or C
		0x5C : BOX_PROJ_ATTACK, # qcf,hcb+AC
		0x5D : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Vice") : {
		0x56 : BOX_THROW,       # hcb,f+A or C
		0x57 : BOX_THROW,       # hcb,f+AC
		0x58 : BOX_THROW,       # hcb,hcb+B or D
		0x59 : BOX_THROW,       # hcb,hcb+BD
		0x5A : BOX_THROW,       # C throw, D throw
		0x5C : BOX_THROW,       # dp+A or C
		0x5E : BOX_THROW,       # dp+AC
		0x5F : BOX_THROW,       # hcf,uf,u,d+A or C (midair)
	},
	IDbyName("Terry") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x65 : BOX_PROJ_ATTACK, # qcf+A
		0x66 : BOX_PROJ_ATTACK, # qcf+C
		0x67 : BOX_PROJ_ATTACK, # qcf+AC
		0x5A : BOX_PROJ_ATTACK, # qcb,db,f+A or C
		0x5B : BOX_PROJ_ATTACK, # qcb,db,f+AC
		0x5C : BOX_PROJ_ATTACK, # qcb,db,f+AC (last hit)
		0x6E : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x6F : BOX_PROJ_ATTACK, # qcf,qcf+AC (after MAX cancel, moves usually get anywhere juggle properties when maxcancelled, so they have different IDs)
		0x52 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Andy") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x68 : BOX_PROJ_ATTACK, # qcb+A or C
		0x6A : BOX_PROJ_ATTACK, # qcb+AC
		0x70 : BOX_PROJ_ATTACK, # qcf,hcb+A (this attackbox overlaps EXACTLY with the vulnbox, no idea how to display that yet)
		0x71 : BOX_PROJ_ATTACK, # qcf,hcb+A (final hit)
		0x52 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Joe") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x64 : BOX_PROJ_ATTACK, # hcf+A or C
		0x66 : BOX_PROJ_ATTACK, # hcf+AC
		0x67 : BOX_PROJ_ATTACK, # hcf+AC (final hit) and qcf,qcf+A or C
		0x68 : BOX_PROJ_ATTACK, # qcf,qcf+A or C (follow up hits)
		0x69 : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x6F : BOX_PROJ_ATTACK, # qcf,hcb+A or C
		0x72 : BOX_PROJ_ATTACK, # qcf,hcb+BD
		0x6A : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Athena") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x67 : BOX_PROJ_ATTACK, # qcb+A
		0x68 : BOX_PROJ_ATTACK, # qcb+C
		0x69 : BOX_PROJ_ATTACK, # qcb+AC
		#0x54 : BOX_PROJ_VULN,   # qcb+B Reflector box, looks like a hurt box (blue), but must be the reflecting bit, won't change color
		0x6A : BOX_THROW,       # hcf+A or C or AC
		0x6D : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Kensou") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x73 : BOX_PROJ_ATTACK, # qcb+A or C
		0x74 : BOX_PROJ_ATTACK, # qcb+AC
		0x75 : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x69 : BOX_PROJ_ATTACK, # qcb,qcb+A or C
		0x6A : BOX_PROJ_ATTACK, # qcb,qcb+AC
		0x6F : BOX_THROW,       # qcf,hcb+A or C
		0x67 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Chin") : {
		0x42 : BOX_PROJ_VULN,   # 
		0x59 : BOX_THROW,       # C throw, D throw, C throw in either stance
		0x74 : BOX_PROJ_ATTACK, # qcf,qcf+BD (neomax) (grounded or midair)
	},
	IDbyName("Kim") : {
		0x54 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Hwa Jai") : {
		0x6A : BOX_THROW,       # qcf,qcb+A or C (drunk or sober)
		0x6B : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Raiden") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x52 : BOX_THROW,       # C throw, D throw
		0x56 : BOX_THROW,       # hcf+B or D
		0x57 : BOX_THROW,       # hcf+BD
		0x5D : BOX_THROW,       # hcb,hcb+A or C
		0x5E : BOX_THROW,       # hcb,hcb+AC
		0x53 : BOX_PROJ_ATTACK, # qcb+A
		0x54 : BOX_PROJ_ATTACK, # qcb+C (on hit/block)
		0x55 : BOX_PROJ_ATTACK, # qcb+AC
	},
	IDbyName("Ryo") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		0x84 : BOX_PROJ_ATTACK, # qcf+A
		0x85 : BOX_PROJ_ATTACK, # qcf+C
		0x86 : BOX_PROJ_ATTACK, # qcf+AC
		0x83 : BOX_PROJ_ATTACK, # qcf,hcb+AC
		0x52 : BOX_THROW,		# C throw, D throw

	},
	IDbyName("Robert") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 43 and 40 always seem to be overlapping with projectiles. I wonder what the difference is
		0x75 : BOX_PROJ_ATTACK, # qcf+A or C
		0x76 : BOX_PROJ_ATTACK, # Not seen, presumably second hit of qcf+AC, hard to make visible.
		0x77 : BOX_PROJ_ATTACK, # qcf+AC
		0x78 : BOX_PROJ_ATTACK, # Not found, presumably a projectile too though.
		0x79 : BOX_PROJ_ATTACK, # f,hcf+P
		0x5F : BOX_THROW,		# hcf+B or D or BD
		0x52 : BOX_THROW,		# C throw, D throw
	},
	IDbyName("Takuma") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		0x3F : BOX_PROJ_VULN,   # qcf+B or D
		0x52 : BOX_PROJ_ATTACK, # qcf+A
		0x53 : BOX_PROJ_ATTACK, # qcf+C
		0x54 : BOX_PROJ_ATTACK, # qcf+AC
		#0x55 : BOX_PROJ_ATTACK, # qcf+B I think these are actual attack boxes, and that these movese actually beat out.
		#0x56 : BOX_PROJ_ATTACK, # qcf+D
		#0x57 : BOX_PROJ_ATTACK, # qcf+BD
		0x66 : BOX_PROJ_ATTACK, # hcf,f+A or C
		0x67 : BOX_PROJ_ATTACK, # hcf,f+C
		0x6B : BOX_PROJ_ATTACK, # qcf,hcb+A
		0x68 : BOX_THROW,       # hcb+B or BD
		0x69 : BOX_THROW,       # hcb+D
		0x65 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Ralf") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		#0x5A : BOX_PROJ_ATTACK, # qcb+A (physical hits)
		#0x5B : BOX_PROJ_ATTACK, # qcb+C (physical hits)
		#0x5C : BOX_PROJ_ATTACK, # qcb+AC (physical hits)
		#0x5D : BOX_PROJ_ATTACK, # qcb+AC (last hit) (physical hits)
		0x52 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Clark") : {
		0x52 : BOX_THROW,       # hcf+B or D
		0x53 : BOX_THROW,       # hcf+BD
		0x5D : BOX_THROW,       # hcb,hcb+A or C
		0x5F : BOX_THROW,       # hcb,hcb+AC
		0x61 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Leona") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x63 : BOX_PROJ_ATTACK, # [b],f+A
		0x64 : BOX_PROJ_ATTACK, # [b],f+C
		0x65 : BOX_PROJ_ATTACK, # [b],f+AC
		0x66 : BOX_PROJ_ATTACK, # qcb+B or D
		0x67 : BOX_PROJ_ATTACK, # qcb+BD
		0x6C : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Mai") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x52 : BOX_PROJ_ATTACK, # qcf+A
		0x53 : BOX_PROJ_ATTACK, # qcf+C
		0x54 : BOX_PROJ_ATTACK, # qcf+AC
		0x55 : BOX_PROJ_ATTACK, # qcb+A
		0x57 : BOX_PROJ_ATTACK, # qcb+C
		0x59 : BOX_PROJ_ATTACK, # qcb+AC
		0x65 : BOX_THROW,		# C throw, D throw
	},
	IDbyName("King") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		0x52 : BOX_PROJ_ATTACK, # qcf+B
		0x53 : BOX_PROJ_ATTACK, # qcf+D
		0x54 : BOX_PROJ_ATTACK, # qcf+BD
		0x55 : BOX_PROJ_ATTACK, # j.qcf+B
		0x56 : BOX_PROJ_ATTACK, # j.qcf+D
		0x57 : BOX_PROJ_ATTACK, # j.qcf+BD
		0x61 : BOX_PROJ_ATTACK, # qcf,qcf+B or D
		0x6B : BOX_PROJ_ATTACK, # qcb,qcb+BD
		0x6C : BOX_THROW,		# C throw, D throw
	},
	IDbyName("Yuri") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		0x52 : BOX_PROJ_VULN,   # qcf+A
		0x53 : BOX_PROJ_VULN,   # qcf+C
		0x54 : BOX_PROJ_VULN,   # qcf+AC
		0x55 : BOX_PROJ_VULN,   # qcf+B
		0x56 : BOX_PROJ_VULN,   # qcf+D
		0x57 : BOX_PROJ_VULN,   # qcf+BD
		0x58 : BOX_PROJ_VULN,   # j.qcf+B
		0x59 : BOX_PROJ_VULN,   # j.qcf+D
		0x5A : BOX_PROJ_VULN,   # j.qcf+BD
		0x5B : BOX_PROJ_ATTACK, # qcb+A
		0x5C : BOX_PROJ_ATTACK, # qcb+C
		0x5D : BOX_PROJ_ATTACK, # qcb+AC
		0x87 : BOX_PROJ_ATTACK, # qcb,qcb+AC
		0x68 : BOX_THROW,       # C throw, D throw
		0x71 : BOX_THROW,       # hcb+B or D
		#dp+K > A+C is her anywhere juggle airthrow. Not sure if we should give that an air-throw bx at all. But I don't see a box showing up at all which is unexpected.
	},
	IDbyName("EX Iori") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x54 : BOX_PROJ_ATTACK, # qcf+A
		0x55 : BOX_PROJ_ATTACK, # qcf+C
		0x56 : BOX_PROJ_ATTACK, # qcf+AC
		0x88 : BOX_PROJ_ATTACK, # qcf,qcf+A
		0x89 : BOX_PROJ_ATTACK, # qcf,qcf+A
		0x6E : BOX_THROW,       # hcb,f+A or C or AC
		0x82 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("K\'") : {
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x52 : BOX_PROJ_ATTACK, # qcf+A
		0x53 : BOX_PROJ_ATTACK, # qcf+C
		0x54 : BOX_PROJ_ATTACK, # qcf+AC
		0x55 : BOX_PROJ_ATTACK, # qcf+A or C > f+B
		0x56 : BOX_PROJ_ATTACK, # qcf+AC > f+B
		0x57 : BOX_PROJ_ATTACK, # qcf+A or C > f+D
		0x58 : BOX_PROJ_ATTACK, # qcf+AC > f+D
		0x70 : BOX_PROJ_ATTACK, # qcf,hcb+A or C
		0x79 : BOX_PROJ_ATTACK, # qcf,hcb+AC
		0x8E : BOX_PROJ_ATTACK, # hcb,hcb+AC
		0x8F : BOX_PROJ_ATTACK, # hcb,hcb+AC (MAX cancelled)
		0x6E : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Kula") : {
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x5F : BOX_PROJ_ATTACK, # qcf+A
		0x60 : BOX_PROJ_ATTACK, # qcf+C
		0x61 : BOX_PROJ_ATTACK, # qcf+AC
		0x63 : BOX_PROJ_ATTACK, # qcb+A or C
		0x65 : BOX_PROJ_ATTACK, # qcb+AC
		0x6A : BOX_PROJ_ATTACK, # qcb+B or D, f+B
		0x6F : BOX_PROJ_ATTACK, # qcb+BD, f+B
		0x71 : BOX_PROJ_ATTACK, # qcf,qcf+A or C
		0x72 : BOX_PROJ_ATTACK, # qcf,qcf+AC
		#0x73 : BOX_PROJ_ATTACK, # not found
		0x74 : BOX_PROJ_ATTACK, # hcb,hcb+AC (diana)
		0x75 : BOX_PROJ_ATTACK, # hcb,hcb+AC or BD (followup) 
		0x76 : BOX_PROJ_ATTACK, # hcb,hcb+AC (diana)
		0x79 : BOX_PROJ_ATTACK, # hcb,hcb+AC (diana second time)
		0x7A : BOX_PROJ_ATTACK, # hcb,hcb+AC (foxy)
		0x7C : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Maxima") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x52 : BOX_PROJ_ATTACK, # qcb+A
		0x54 : BOX_PROJ_ATTACK, # qcb+AC (1st hit)
		0x56 : BOX_PROJ_ATTACK, # qcb+AC (2nd hit)
		0x6A : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x6C : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x6D : BOX_PROJ_ATTACK, # qcf,qcf+AC
		0x71 : BOX_PROJ_ATTACK, # hcb,hcb+AC
		0x5B : BOX_THROW,		# hcb+B or D
		0x63 : BOX_THROW,		# C throw, D throw
	},
	# characters not associated with a team; hidden, DLC
	IDbyName("EX Kyo") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x6E : BOX_PROJ_ATTACK, # qcb,hcf+A or C
		0x6F : BOX_PROJ_ATTACK, # qcb,hcf+AC
		0x89 : BOX_PROJ_ATTACK, # qcf,qcf+ A or C
		0x52 : BOX_THROW,       # C throw, D throw (same as regular Kyo)
	},
	#IDbyName("EX Iori") : {
	#	#,
	#},
	IDbyName("Mr. Karate") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   #
		0x52 : BOX_PROJ_ATTACK, # qcf A
		0x53 : BOX_PROJ_ATTACK, # qcf C
		0x54 : BOX_PROJ_ATTACK, # qcf AC
		0x65 : BOX_PROJ_ATTACK, # hcf,f+A or C
		0x77 : BOX_PROJ_ATTACK, # qcf,hcb+A or C
		0x84 : BOX_PROJ_ATTACK, # qcf,hcb+AC
		0x9A : BOX_THROW,       # hcb+B or D
		0x9C : BOX_THROW,       # hcb+BD
		0x63 : BOX_THROW,       # C throw, D throw
	},
	IDbyName("Billy") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x65 : BOX_PROJ_ATTACK, # qcf,hcb+A or C
		0x66 : BOX_PROJ_ATTACK, # qcf,hcb+A or C (followup)
		0x67 : BOX_PROJ_ATTACK, # qcf,hcb+AC
		0x68 : BOX_PROJ_ATTACK, # qcf,hcb+AC (followup)
		0x72 : BOX_PROJ_ATTACK, # qcf,qcf+AC
		# BOX_PROJ_ATTACK, # Big full screen fireball at the end of  the neomax can't be 
		0x6D : BOX_THROW,		# C throw, D throw (Billy's throwbox is WAY bigger than other characters')
	},
	IDbyName("Ash") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x55 : BOX_PROJ_ATTACK, # [b],f+A
		#0x56 : BOX_PROJ_ATTACK, # [b],f+C (physical hit)
		#0x57 : BOX_PROJ_ATTACK, # [b],f+C (2nd hit) (physical hit)
		0x58 : BOX_PROJ_ATTACK, # [b],f+C (projectile)
		#0x59 : BOX_PROJ_ATTACK, # [b],f+AC (physical hit)
		0x5C : BOX_PROJ_ATTACK, # [b],f+AC (projectile)
		0x68 : BOX_PROJ_ATTACK, # qcf,qcf+A or C
		0x69 : BOX_PROJ_ATTACK, # qcf,qcf+A or C (follow up)
		0x6F : BOX_PROJ_ATTACK, # qcb+A or B or C or D
		0x70 : BOX_PROJ_ATTACK, # qcb+AC or BD
		0x71 : BOX_PROJ_ATTACK, # qcb+AC or BD (2nd hit)
		0x6B : BOX_PROJ_ATTACK, # A~B~C~D
		0x6C : BOX_THROW,       # hcb,hcb+BD
		0x72 : BOX_THROW,		# C throw, D throw
	},
	IDbyName("Saiki") : {
		0x3F : BOX_PROJ_VULN,   # 
		0x40 : BOX_PROJ_VULN,   # 
		0x41 : BOX_PROJ_VULN,   # 
		0x42 : BOX_PROJ_VULN,   # 
		0x43 : BOX_PROJ_VULN,   # 
		0x58 : BOX_PROJ_ATTACK, # qcf+A
		0x5B : BOX_PROJ_ATTACK, # qcf+C
		0x5E : BOX_PROJ_ATTACK, # qcf+AC
		0x91 : BOX_PROJ_ATTACK, # qcf,qcf+A or C
		0x86 : BOX_THROW,		# hcb,hcb+A or C
		0x87 : BOX_THROW,		# hcb,hcb+AC
		0x7C : BOX_THROW,		# C throw, D throw
		#The qcb,hcb+AC Neomax is fullscreen, and the vulnerable fireball box overlaps the red fireball box. Don't know what the number is.
	},
}
