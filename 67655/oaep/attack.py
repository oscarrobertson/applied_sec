#!/usr/bin/env python

import sys , subprocess, os.path, math

def interact( l, c ) :
	# Send l to attack target.
	target_in.write( "%s\n" % ( l ) ) ; target_in.flush()
	# Send c to attack target.
	target_in.write( "%s\n" % ( c ) ) ; target_in.flush()
	# Receive r from attack target.
	r = int( target_out.readline().strip () )
	return r

def readConf(confName):
	pathStr = os.path.abspath(confName)
	with open(pathStr, "r") as f:
		n = f.readline().strip()
		e = f.readline().strip()
		l = f.readline().strip()
		c = f.readline().strip()
	return (n, e, l, c)


def step1(n, e, l, c):
	f1 = 2

	while True:
		c_modified = (c * pow(f1, e, n))%n
		r = interact(l, format(c_modified, "X"))
		if r == 1:
			f1 = f1 << 1
		elif r == 2 or r == 4:
			break;
		else:
			raise Exception("Result other than 0 or 1, r = " + str(r))
		print f1

	return f1

def step2(n, e, l, c, f1):
	k = int(math.ceil(math.log(n, 256)))
	B = pow(2, 8*(k-1))
	f2 = int(math.floor((n+B)/B))*(f1 >> 1)
	loop_count = 0
	while True:
		c_modified = (c * pow(f2, e, n))%n
		print loop_count
		loop_count += 1
		r = interact(l, format(c_modified, "X"))
		if r == 1:
			f2 = f2 + (f1 >> 1)
		elif r == 0:
			break
		else:
			raise Exception("Result other than 0 or 1, r = " + str(r))

	return f2


if ( __name__ == "__main__" ) :
	# Produce a sub -process representing the attack target.
	target = subprocess.Popen( args = os.path.abspath(sys.argv[1]), stdout = subprocess.PIPE , stdin = subprocess.PIPE )
	# Construct handles to attack target standard input and output.
	target_out = target.stdout
	target_in = target.stdin
	# Execute a function 
	(n, e, l, c) = readConf(sys.argv[2])
	n = int(n, 16)
	e = int(e, 16)
	l = "" #int(l, 16)
	c = int(c, 16)
	f1 = step1(n, e, l, c)
	print f1
	##f2 = step2(n, e, l, c, f1)
