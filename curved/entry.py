#!/usr/bin/env python

import sys
import hashlib
import itertools
import string

prefix = sys.argv[1]

for postfix in itertools.product(string.printable, repeat=29-len(prefix)):
	candidate = hashlib.sha1(prefix+"".join(postfix)).hexdigest()
	if(int(candidate, 16) & 0x3FFFFFF == 0x3FFFFFF):
		print("found: {}".format(prefix+"".join(postfix)))
		exit()


