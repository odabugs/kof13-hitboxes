from sys import argv


# return whether the target string was passed in argv
def argvContains(target):
	return target in argv


# return a shallow copy of the dictionary d,
# with the listed keys removed
def dictWithout(d, keys):
	result = d.copy()
	for k in keys:
		del result[k]
	return result


# return the union of all dicts passed,
# with the values in later dicts passed taking priority where keys conflict
def merge(*dicts):
	result = {}
	for d in dicts:
		result.update(d)
	return result


# return the combined set of keys from the union of all dicts passed
def allKeys(*dicts):
	result = set()
	for d in dicts:
		result.update(d.keys())
	return result
