#!/usr/bin/env python
# Tools to fit answers into fixed-byte data.

def pack(data, length, pack=False):
	"""
	Pack data (a sorted list of (score, candidate) into length bytes.

	If pack = True, will continue to look for smaller words to fit in until
	there is no space or no more words.  If pack = False, stops at the first
	word to go over.
	"""
	used_values = []
	output = ""
	for x in data:
		_,s = x
		if len(s) > length:
			if pack:
				pass
			else:
				break
		else:
			used_values.append(x)
			output += " " + s
			length -= len(s) + 1
	for value in used_values:
		data.remove(value)
	return output[1:],data # trim off leading space

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
	out,flat = pack(s, 10, pack=False)
	print ":"+out
	print flat
	out,flat = pack(s, 10, pack=True)
	print ":"+out
	print flat
