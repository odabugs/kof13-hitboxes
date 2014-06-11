from ConfigParser import RawConfigParser
from sys import argv
import os.path

from Colors import *
from Global import *


# supported config options and their defaults are at the bottom of this file
WHITESPACE = " \t" # for passing to str.strip()
ERROR_SUFFIX = "\n  Please refer to README.txt for help with config files."


class Config:
	def __init__(self):
		self.reader = RawConfigParser()
		self.globalConfig = {}
		self.p1config = {}
		self.p2config = {}
	
	
	# if player is not passed then fall back on globalConfig
	def get(self, option, player=None):
		originalOption = option.strip(WHITESPACE)
		option = originalOption.lower()
		if option not in allConfigOptions:
			raise ValueError(
				"The option " + repr(originalOption) +
				" is not recognized." +
				ERROR_SUFFIX)

		g, p1, p2 = self.globalConfig, self.p1config, self.p2config
		lookups = (g)
		fallback = globalDefaults
		if player == 1:
			lookups = (p1, g)
			fallback = playerDefaults
		elif player == 2:
			lookups = (p2, g)
			fallback = playerDefaults

		for lookup in lookups:
			result = lookup.get(option, None)
			if result is not None:
				return result
		else: # if for loop is exhausted
			warnMsg = (
				"WARNING: The option %s has no set value!" +
				"\n  Falling back on this option's default value.")
			print warnMsg % repr(originalOption)
			resultParser, resultRawValue = fallback[option]
			result = resultParser(resultRawValue)
			return result
	

def parseBoolean(value):
	originalValue = value.strip(WHITESPACE)
	value = originalValue.lower()
	trueValues  = set(["1", "true",  "yes", "on" ])
	falseValues = set(["0", "false", "no",  "off"])

	if value in trueValues:
		return True
	elif value in falseValues:
		return False
	else:
		raise ValueError(
			"The value " + repr(originalValue) +
			" could not be interpreted as a boolean." +
			ERROR_SUFFIX)


# read hex (C syntax) or decimal unsigned bytes (we don't need octal support)
def parseUnsignedByte(value):
	originalValue = value.strip(WHITESPACE)
	value = originalValue.lower()
	hexRegex = re.compile("\A0x[0-9a-f]{1,2}\Z")
	decimalRegex = re.compile("\A\d{1,3}\Z")

	result = None
	if hexRegex.match(value):
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


def parseInt(value, base=10, positiveOnly=True):
	value = value.strip(WHITESPACE)
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
			newError("The entry '" + entry + "' (entry #%d) is invalid." % i)
	
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


# the following values can be set globally or individually per player;
# options set on a per-player basis override the same options set globally
# map structure:
# option name : (reader function, default value)
playerDefaults = {
	"enabled" : (parseBoolean, "yes"),
	"draw_box_fill" : (parseBoolean, "yes"),
	"draw_box_borders" : (parseBoolean, "yes"),
	"draw_pivot" : (parseBoolean, "yes"),
	"fill_opacity" : (parseUnsignedByte, "0x40"),
	"border_opacity" : (parseUnsignedByte, "0xFF"),
	"pivot_radius" : (parseInt, "20"),
	"pivot_opacity" : (parseUnsignedByte, "0xFF"),
	"pivot_color" : (parseColor, "white"),
	"collision_box_color" : (parseColor, "cyan"),
	"vulnerable_box_color" : (parseColor, "blue"),
	"attack_box_color" : (parseColor, "red"),
	"guard_box_color" : (parseColor, "green"),
	"throw_box_color" : (parseColor, "magenta"),
	"projectile_vulnerable_box_color" : (parseColor, "yellow"),
	"projectile_attack_box_color" : (parseColor, "orange"),
	}

# ordered from lowest to highest drawing priority; higher overlaps lower
defaultDrawOrder = (
	"collision",
	"vulnerable",
	"attack",
	"guard",
	"throw",
	"projectile_vulnerable",
	"projectile_attack",
	"pivot"
	)

# "enabled" is only intended to turn off rendering on a per-player basis;
# "draw_order" is intended to apply to both players alike
globalDefaults = merge(
	dictWithout(playerDefaults, ["enabled"]),
	{"draw_order" : (parseDrawOrder, ", ".join(defaultDrawOrder))})

allConfigOptions = frozenset(allKeys(globalDefaults, playerDefaults))
