from ConfigParser import RawConfigParser
from sys import argv
from os import getcwdu
import os.path
import re

from Colors import colorByName, colorAsHex, colorAsRGB, printAsRGB
from Global import *


# supported config options and their defaults are at the bottom of this file
WHITESPACE = " \t" # for passing to str.strip()
ERROR_SUFFIX = "\n  Please refer to README.txt for help with config files."
DEFAULT_CONFIG = os.path.join(getcwdu(), "default.cfg")
GLOBAL_SECTION = "Global"
P1_SECTION, P2_SECTION = "Player1", "Player2"


class Config:
	def __init__(self, configFile=None):
		self.reader = RawConfigParser()
		self.globalConfig = {}
		self.p1config = {}
		self.p2config = {}
		
		if configFile is not None:
			self.loadFromFile(configFile)
	

	def getGlobal(self, option):
		originalOption = option.strip(WHITESPACE)
		option = originalOption.lower()

		if option not in globalOptions:
			raise ValueError(
				"The global config option " + repr(originalOption) +
				" is not recognized." +
				ERROR_SUFFIX)

		result = self.globalConfig.get(option, None)
		if result is None:
			result = globalDefaults[option]
			self.globalConfig[option] = result
		return result


	def getPlayer(self, option, player):
		originalOption = option.strip(WHITESPACE)
		option = originalOption.lower()

		if player == 1:
			playerCfg = self.p1config
		elif player == 2:
			playerCfg = self.p2config
		else:
			raise ValueError("player parameter must be 1 or 2")

		if option not in playerOptions:
			raise ValueError(
				"The player config option " + repr(originalOption) +
				" is not recognized." +
				ERROR_SUFFIX)

		lookupOrder = (playerCfg, self.globalConfig, playerDefaults)
		for lookup in lookupOrder:
			result = lookup.get(option, None)
			if result is not None:
				playerCfg[option] = result
				return result
	

	def get(self, option, player=None):
		if player is None:
			return self.getGlobal(option)
		elif player in (1, 2):
			return self.getPlayer(option, player)
		else:
			raise ValueError("player must be 1, 2 or None (global)")
	
	
	# for REPL class testing only
	def printout(self):
		def printWithSelectKeys(m, keysToPrint):
			result = "{"
			for k in keysToPrint:
				if "color" in k:
					printFn = printAsRGB
				else:
					printFn = repr
				result += "\n\t%s: %s" % (k, printFn(m.get(k)))
			result += "\n}"
			print result

		print "Global:"
		printWithSelectKeys(self.globalConfig, globalOptions)
		print " ----- "
		print "Player 1:"
		printWithSelectKeys(self.p1config, playerOptions)
		print " ----- "
		print "Player 2:"
		printWithSelectKeys(self.p2config, playerOptions)
	
	
	# TODO: add error checking (missing file, bad sections/options, etc.)
	def loadFromFile(self, filePath=DEFAULT_CONFIG):
		cfg = self.reader
		cfg.read(filePath)

		def fillGlobalConfig():
			for option in globalOptions:
				typeParser, defaultValue = rawGlobalDefaults[option]
				toStore = None
				try:
					toStore = typeParser(cfg.get(GLOBAL_SECTION, option))
				except Exception as e:
					print e.message
					toStore = None
				finally:
					if toStore is None:
						toStore = typeParser(defaultValue)
					self.globalConfig[option] = toStore

		def fillPlayerConfig(player):
			ps = {
				1 : (P1_SECTION, self.p1config),
				2 : (P2_SECTION, self.p2config)
				}
			section, playerConfig = ps[player]
			for option in playerOptions:
				typeParser, defaultValue = rawPlayerDefaults[option]
				toStore = None
				try:
					toStore = typeParser(cfg.get(section, option))
				except Exception as e:
					print e.message
					toStore = self.globalConfig[option]
				finally:
					playerConfig[option] = toStore

		fillGlobalConfig()
		fillPlayerConfig(1)
		fillPlayerConfig(2)


def parseBoolean(value):
	originalValue = value.strip(WHITESPACE)
	value = originalValue.lower()
	trueValues  = set(["1", "true",  "yes", "on" ])
	falseValues = set(["0", "false", "no",  "off"])

	if len(value) == 0:
		return None
	elif value in trueValues:
		return True
	elif value in falseValues:
		return False
	else:
		raise ValueError(
			"The value " + repr(originalValue) +
			" could not be interpreted as a boolean." +
			ERROR_SUFFIX)


# read hex (C syntax) or decimal unsigned bytes
def parseUnsignedByte(value):
	originalValue = value.strip(WHITESPACE)
	value = originalValue.lower()
	hexRegex = re.compile("\A0x[0-9a-f]{1,2}\Z")
	decimalRegex = re.compile("\A\d{1,3}\Z")

	result = None
	if len(value) == 0:
		return None
	elif hexRegex.match(value):
		result = int(value, 16)
	elif decimalRegex.match(value):
		result = int(value, 10)
	
	if result is None or result < 0 or result > 255:
		raise ValueError(
			"The value " + repr(originalValue) +
			" could not be interpreted as an integer from 0-255." +
			ERROR_SUFFIX)
	else:
		return result


# do we even use this now?
def parseInt(value, base=10, positiveOnly=True):
	value = value.strip(WHITESPACE)
	if len(value) == 0:
		return None

	result = None
	try:
		result = int(value, base)
	except:
		raise ValueError(
			"The value " + repr(value) +
			" could not be interpreted as an integer." +
			ERROR_SUFFIX)

	if positiveOnly and result < 0:
		raise ValueError(
			"The value " + repr(value) +
			" may not be a negative number." +
			ERROR_SUFFIX)
	else:
		return result


def parseColor(value):
	originalValue = value.strip(WHITESPACE)
	value = originalValue.lower()
	if len(value) == 0:
		return None

	colorStringParsers = (colorByName, colorAsHex, colorAsRGB)
	for parser in colorStringParsers:
		result = parser(value)
		if result is not None:
			return result
	else: # if the above loop is exhausted
		raise ValueError(
			"The value " + repr(originalValue) +
			" could not be interpreted as a color." +
			ERROR_SUFFIX)


def parseDrawOrder(value):
	if len(value) == 0:
		return None

	clean = lambda s: s.strip(WHITESPACE).lower()
	splitValue = [clean(item) for item in value.split(",")]
	
	# check for invalid, missing or duplicated entries in value list
	orderCounts = dict([(key, 0) for key in defaultDrawOrder])
	errorsList = []
	newError = lambda err: errorsList.append(" - " + err) # side-effecting

	i = 0
	for entry in splitValue:
		i += 1
		if entry in orderCounts:
			orderCounts[entry] += 1
		else:
			newError("The entry '%s' (entry #%d) is invalid." % (entry, i))
	
	for pair in orderCounts.iteritems():
		entry, count = pair
		if count == 0:
			newError("The entry '" + entry + "' is missing.")
		elif count > 1:
			newError("The entry '" + entry + "' appears more than once.")
	
	if len(errorsList) > 0:
		raise ValueError(
			"The following errors were found in draw_order:\n" +
			"\n".join(errorsList) +
			ERROR_SUFFIX)
	else:
		return tuple(splitValue)


# probably the least messy code in this file
def processMap(m):
	result = {}
	for key, value in m.items():
		parser, rawValue = value
		result[key] = parser(rawValue)
	return result


# these options can be set globally (see globalOptions) or per player;
# options set on a per-player basis override the same options set globally
# map structure:
# option name : (reader function, default value)
rawPlayerDefaults = {
	"enabled" : (parseBoolean, "yes"),
	"collision_box_color" : (parseColor, "cyan"),
	"vulnerable_box_color" : (parseColor, "blue"),
	"attack_box_color" : (parseColor, "red"),
	"guard_box_color" : (parseColor, "green"),
	"throw_box_color" : (parseColor, "magenta"),
	"throwable_box_color" : (parseColor, "white"),
	"projectile_vulnerable_box_color" : (parseColor, "yellow"),
	"projectile_attack_box_color" : (parseColor, "orange"),
	}
playerDefaults = processMap(rawPlayerDefaults)
playerOptions = tuple(playerDefaults.keys())

# ordered from lowest to highest drawing priority; higher overlaps lower,
# pivot is implicit and always has the highest priority (i.e., is drawn last)
defaultDrawOrder = (
	"collision",
	"vulnerable", # hurtbox
	"throwable",
	"attack", # hitbox
	"guard", # for blocking and for moves with armor points
	"throw",
	"proj_vulnerable", # projectile hurtbox
	"proj_attack", # projectile hitbox
	)

# options that can be set globally but not on a per-player basis
globalOnlyDefaults = {
	"draw_box_borders" : (parseBoolean, "yes"),
	"box_border_opacity" : (parseUnsignedByte, "0xFF"),
	"draw_box_fill" : (parseBoolean, "yes"),
	"box_fill_opacity" : (parseUnsignedByte, "0x40"),
	"draw_pivots" : (parseBoolean, "yes"),
	"pivot_opacity" : (parseUnsignedByte, "0xFF"),
	"pivot_radius" : (parseUnsignedByte, "20"),
	"pivot_color" : (parseColor, "white"),
	"draw_order" : (parseDrawOrder, ",".join(defaultDrawOrder)),
	}

# "enabled" is only intended to turn off rendering on a per-player basis
rawGlobalDefaults = merge(
	dictWithout(rawPlayerDefaults, ["enabled"]),
	globalOnlyDefaults)
globalDefaults = processMap(rawGlobalDefaults)
globalOptions = tuple(globalDefaults.keys())

allConfigOptions = frozenset(allKeys(globalDefaults, playerDefaults))
