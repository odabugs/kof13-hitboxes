from ConfigParser import RawConfigParser
from sys import argv
import os.path

from Colors import *
from Global import *


class Config:
	def __init__(self):
		self.reader = RawConfigParser()
	

def parseBoolean(value):
	lowerValue = value.lower()
	trueValues  = set(["1", "true",  "yes", "on" ])
	falseValues = set(["0", "false", "no",  "off"])

	if lowerValue in trueValues:
		return True
	elif lowerValue in falseValues:
		return False
	else:
		raise ValueError("The value " + repr(value) +
		" could not be interpreted as a boolean.")


# read hex (C syntax) or decimal unsigned bytes (we don't need octal support)
def parseUnsignedByte(value):
	hexRegex = re.compile("\A(0x[0-9a-f]{1,2})\Z", re.IGNORECASE)
	decimalRegex = re.compile("\A\d{1,3}\Z")

	result = None
	if hexRegex.match(value):
		result = int(value, 16)
	elif decimalRegex.match(value):
		result = int(value, 10)
	
	if result is None or result < 0 or result > 255:
		raise ValueError("The value " + repr(value) +
		" could not be interpreted as an integer from 0-255.")
	else:
		return result


def parseInt(value, base=10, positiveOnly=True):
	result = None
	try:
		result = int(value, base)
	except ValueError as e:
		raise e

	if positiveOnly and result < 0:
		raise ValueError("The value " + repr(value) +
		" may not be a negative number.")
	else:
		return result


def parseColor(value):
	colorStringParsers = (colorByName, colorAsHex, colorAsRGB)
	for parser in colorStringParsers:
		result = parser(value)
		if result is not None:
			return result

	raise ValueError("The value " + repr(value) +
	" could not be interpreted as a color.")


# map structure:
# option name : (reader function, default value)
playerConfigOptions = {
	"enabled" : (parseBoolean, True),
	"draw_pivot" : (parseBoolean, True),
	"draw_box_fill" : (parseBoolean, False),
	"draw_box_borders" : (parseBoolean, True),
	"pivot_size" : (parseInt, 20),
	"pivot_opacity" : (parseUnsignedByte, 0xFF),
	"fill_opacity" : (parseUnsignedByte, 0x40),
	"border_opacity" : (parseUnsignedByte, 0xFF),
	"pivot_color" : (parseColor, colorByName("white")),
	"collision_box_color" : (parseColor, colorByName("cyan")),
	"vulnerable_box_color" : (parseColor, colorByName("blue")),
	"attack_box_color" : (parseColor, colorByName("red")),
	"guard_box_color" : (parseColor, colorByName("green")),
	"throw_box_color" : (parseColor, colorByName("magenta")),
	"projectile_vulnerable_box_color" : (parseColor, colorByName("yellow")),
	"projectile_attack_box_color" : (parseColor, colorByName("orange")),
	}

# options set on a per-player basis override the same options set globally;
# "enabled" is only intended to turn off rendering on a per-player basis
globalConfigOptions = dictWithout(playerConfigOptions, "enabled")

