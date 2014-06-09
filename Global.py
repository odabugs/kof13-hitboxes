from sys import argv


# return whether the target string was passed in argv
def argvContains(target):
	return target in argv


# return a shallow copy of the dictionary d,
# with the keys listed in the following arguments removed
def dictWithout(d, *keys):
	result = d.copy()
	for k in keys:
		del result[k]
	return result
