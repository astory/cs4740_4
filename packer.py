#!/usr/bin/env python
# Tools to fit answers into fixed-byte data.

def pack(data, length, pack=False):
	"""
	Pack data (which is some ordered grouping of strings, with arbitrary
	nesting, into length bytes.

	If pack = True, will continue to look for smaller words to fit in until
	there is no space or no more words.  If pack = False, stops at the first
	word to go over.
	"""
	flat = flatten(data)
	output = ""
	for x in flat:
		if len(x) > length:
			if pack:
				pass
			else:
				break
		else:
			output += " " + x
			length -= len(x) + 1
	return output[1:] # trim off leading space

def flatten(data):
	"""
	Turn an arbitrary nesting of objects in lists into a flat list of strings
	"""
	output = []
	for x in data:
		if isinstance(x, list):
			output.extend(flatten(x))
		else:
			output.append(x)
	return output

if __name__ == "__main__":
	s = ["hello", ["to", ["you"], ["there"]]]
	print flatten(s)

	s = ["a", "bb", "ccc", "dddd", "e"]
	print ":"+pack(s, 10, pack=False)
	print ":"+pack(s, 10, pack=True)
