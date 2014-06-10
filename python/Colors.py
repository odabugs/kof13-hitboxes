import re


A_POS, R_POS, G_POS, B_POS = 24, 16, 8, 0
A_MASK = (0xFF << A_POS)
R_MASK = (0xFF << R_POS)
G_MASK = (0xFF << G_POS)
B_MASK = (0xFF << B_POS)
RGB_MASK = R_MASK | G_MASK | B_MASK


def rgb(red, green, blue, alpha=255):
	red, green, blue = int(red), int(green), int(blue)

	outOfRange = lambda x: x < 0 or x > 255
	if len(filter(outOfRange, (red, green, blue, alpha))) > 0:
		raise ValueError("red, green, blue and alpha must all be " +
		"between 0 and 255 inclusive.")
	else:
		return (alpha << A_POS) | (red << R_POS) | (green << G_POS) | blue


# wedged in the middle for REPL testing
# (python doesn't have forward declarations)
colorsByName = {
	"white"     : rgb(0xFF, 0xFF, 0xFF),
	"silver"    : rgb(0xC0, 0XC0, 0XC0),
	"gray"      : rgb(0X80, 0x80, 0x80),
	"grey"      : rgb(0X80, 0x80, 0x80), # alternative to "gray"
	"black"     : rgb(0x00, 0x00, 0x00),
	"red"       : rgb(0xFF, 0x00, 0x00),
	"green"     : rgb(0x00, 0xFF, 0x00),
	"blue"      : rgb(0x00, 0x00, 0xFF),
	"yellow"    : rgb(0xFF, 0xFF, 0x00),
	"magenta"   : rgb(0xFF, 0x00, 0xFF),
	"fuchsia"   : rgb(0xFF, 0x00, 0xFF), # alternative to "magenta"
	"cyan"      : rgb(0x00, 0xFF, 0xFF),
	"pink"      : rgb(0xFF, 0xC0, 0xC0),
	"orange"    : rgb(0xFF, 0x80, 0x00),
	"darkred"   : rgb(0x80, 0x00, 0x00),
	"darkgreen" : rgb(0x00, 0x80, 0x00),
	"darkblue"  : rgb(0x00, 0x00, 0x80),
	"brown"     : rgb(0x80, 0x80, 0x00),
	"purple"    : rgb(0x80, 0x00, 0x80),
	"teal"      : rgb(0x00, 0x80, 0x80),
	"turquoise" : rgb(0x00, 0x80, 0x80), # alternative to "teal"
	}


def colorByName(colorName, alpha=255):
	if alpha < 0 or alpha > 255:
		raise ValueError("alpha must be between 0 and 255 inclusive.")
	
	result = colorsByName.get(colorName.lower(), None)
	if result is not None:
		result = result | (alpha << A_POS)


def colorAsHex(value, alpha=255):
	hexRegex = re.compile("\A#[0-9a-f]{6}\Z", re.I) # IGNORECASE
	
	if alpha < 0 or alpha > 255:
		raise ValueError("alpha must be between 0 and 255 inclusive.")

	if not hexRegex.match(value):
		return None
	else:
		return int(value[1:], 16) | (alpha << A_POS)


def colorAsRGB(value, alpha=255):
	RGBRegex = re.compile("\Argb\(\d{1,3},\d{1,3},\d{1,3}\)\Z", re.I)
	
	if alpha < 0 or alpha > 255:
		raise ValueError("alpha must be between 0 and 255 inclusive.")

	if not RGBRegex.match(value):
		return None
	else:
		# reduce string from "rgb(X, Y, Z)" down to "X, Y, Z"
		beginIndex = value.find("(") + 1
		endIndex = value.find(")")
		subvalues = value[beginIndex:endIndex].split(",")
		red, green, blue = [int(v) for v in subvalues]
		
		result = None
		try:
			result = rgb(red, green, blue)
		except ValueError:
			result = None
		
		if result is not None:
			result = result | (alpha << A_POS)
		return result


def changeAlpha(color, newAlpha):
	if newAlpha < 0 or newAlpha > 255:
		raise ValueError("New alpha must be between 0 and 255 inclusive.")
	return (color & RGB_MASK) | (newAlpha << A_POS)
