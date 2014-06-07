# python is too stupid to handle files mutually importing symbols from
# each other, making this file necessary
# TODO: get rid of this, replace it with a class that reads and parses configs
from sys import argv

def argvContains(target):
	return target in argv
