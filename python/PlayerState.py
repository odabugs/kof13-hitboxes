from CStructures import PLAYER, PLAYER_TEAM, HITBOX_SET, HITBOX1, HITBOX2
from BoxTypes import nameByID, hitboxTypes, attackBoxFn, armorBoxFn
from BoxTypes import collisionBoxFn, vulnerableBoxFn, proximityBoxFn


class PlayerState:
	def __init__(self, environment, ID, playerPtr, teamPtr, hitboxesPtr):
		self.env = environment
		self.process = self.env.process
		self.ID = ID # am I player 1 or 2?
		self.playerPtr = playerPtr
		self.teamPtr = teamPtr
		self.hitboxesPtr = hitboxesPtr

		self.playerStruct = PLAYER()
		self.teamStruct = PLAYER_TEAM()
		self.hitboxesStruct = HITBOX_SET()
		self.team = [-1, -1, -1] # character IDs of player team
		self.currentChar = -1 # current character's ID

		# HITBOX1 and HITBOX2 have their "next" pointer at different offsets
		self.boxbuf1 = HITBOX1()
		self.boxbuf2 = HITBOX2()
		self.hitboxes = dict([(boxType, []) for boxType in hitboxTypes])
	

	def update(self):
		pstructAddress = self.process.readUnsignedDword(self.playerPtr)
		self.process._RPM(pstructAddress, self.playerStruct)
		self.process._RPM(self.teamPtr, self.teamStruct)
		ps = self.playerStruct

		self.team[0] = self.teamStruct.First
		self.team[1] = self.teamStruct.Second
		self.team[2] = self.teamStruct.Third
		self.currentChar = self.teamStruct.Current

		self.process._RPM(self.hitboxesPtr, self.hitboxesStruct)
		self.updateHitboxes()
	

	def nameTeam(self):
		return ", ".join(map(nameByID, self.team))


	def nameCurrentChar(self):
		return nameByID(self.currentChar)


	# for the list of boxCount boxes starting at (*(*origin))+offset,
	# add each box's coorinates to our internal hitbox set
	# offset should be 0 if boxBuffer is a HITBOX1 and 8 if it's a HITBOX2
	# (why does the game need two nearly identical box structs anyway?)
	def readHitboxList(self, origin, offset, boxCount, boxBuffer, boxTypeFn):
		readPointer = self.process.readUnsignedDword
		readNextBoxFrom = lambda address: self.process._RPM(address, boxBuffer)
		readNextBox = lambda: readNextBoxFrom(boxBuffer.Next1 + offset)
		asTuple = lambda b: (b.Left, b.Bottom, b.Width, b.Height)
		#base = readPointer(readPointer(origin)) + offset
		base = readPointer(origin) + offset
		readNextBoxFrom(base)

		for i in range(boxCount):
			boxType = boxTypeFn(self.currentChar, boxBuffer.BoxID)
			self.hitboxes[boxType].append(asTuple(boxBuffer))
			readNextBox()
	

	def updateHitboxes(self):
		# wipe existing hitbox data
		for boxType in hitboxTypes:
			del self.hitboxes[boxType][:]

		# read new hitbox data
		readList = self.readHitboxList
		hbs = self.hitboxesStruct
		buf1, buf2 = self.boxbuf1, self.boxbuf2
		readList(hbs.Collision, 8, hbs.CollisionCount, buf2, collisionBoxFn)
		# hbs.Attack contains attack, throw, proj. attack and proj. vuln boxes
		readList(hbs.Attack, 0, hbs.AttackCount, buf1, attackBoxFn)
		readList(hbs.Armor, 0, hbs.ArmorCount, buf1, armorBoxFn)
		readList(hbs.Vulnerable, 0, hbs.VulnerableCount, buf1, vulnerableBoxFn)
		readList(hbs.Proximity, 8, hbs.ProximityCount, buf2, proximityBoxFn)
