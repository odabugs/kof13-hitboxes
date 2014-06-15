from sys import argv
import functools


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


# interleave an arbitrary number of lists or tuples; result is a tuple
# example: interleave([1, 4], [2, 5], [3, 6]) = (1, 2, 3, 4, 5, 6)
# if sequences are not even in length then the excess elements in all but
# the shortest list passed will be dropped
# example: interleave([1], [2, 4], [3, 5, 6]) = (1, 2, 3)
def interleave(*sequences):
	concat = lambda x, y: x + y
	return functools.reduce(concat, zip(*sequences))
