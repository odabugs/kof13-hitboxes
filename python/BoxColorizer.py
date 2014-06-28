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
		#,
	},
	IDbyName("Duo Lon") : {
		#,
	},
	IDbyName("Shen") : {
		#,
	},
	IDbyName("Kyo") : {
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
		#,
	},
	IDbyName("Iori") : {
		#,
	},
	IDbyName("Mature") : {
		#,
	},
	IDbyName("Vice") : {
		#,
	},
	IDbyName("Terry") : {
		#,
	},
	IDbyName("Andy") : {
		#,
	},
	IDbyName("Joe") : {
		#,
	},
	IDbyName("Athena") : {
		#,
	},
	IDbyName("Kensou") : {
		#,
	},
	IDbyName("Chin") : {
		#,
	},
	IDbyName("Kim") : {
		#,
	},
	IDbyName("Hwa Jai") : {
		#,
	},
	IDbyName("Raiden") : {
		#,
	},
	IDbyName("Ryo") : {
		#,
	},
	IDbyName("Robert") : {
		#,
	},
	IDbyName("Takuma") : {
		#,
	},
	IDbyName("Ralf") : {
		#,
	},
	IDbyName("Clark") : {
		#,
	},
	IDbyName("Leona") : {
		#,
	},
	IDbyName("Mai") : {
		#,
	},
	IDbyName("King") : {
		#,
	},
	IDbyName("Yuri") : {
		#,
	},
	IDbyName("EX Iori") : {
		#,
	},
	IDbyName("K\'") : {
		#,
	},
	IDbyName("Kula") : {
		#,
	},
	IDbyName("Maxima") : {
		#,
	},
	# characters not associated with a team; hidden, DLC
	IDbyName("EX Kyo") : {
		#,
	},
	IDbyName("EX Iori") : {
		#,
	},
	IDbyName("Mr. Karate") : {
		#,
	},
	IDbyName("Billy") : {
		#,
	},
	IDbyName("Ash") : {
		#,
	},
	IDbyName("Saiki") : {
		#,
	},
}
