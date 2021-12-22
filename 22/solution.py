import re
from sys import stdin
import resource
import numpy as np
resource.setrlimit(resource.RLIMIT_AS, (1024*1024*1024*12, resource.RLIM_INFINITY))

def parse(s):
	a, c = s.split("..")
	a, b = a.split("=")
	return int(b), int(c)

commands = []
#X, Y, Z = set(), set(), set()
X, Y, Z = set([-50,51]), set([-50,51]), set([-50,51])
for line in stdin:
	state, xyz = line.strip().split(" ")
	x, y, z = map(parse, xyz.split(","))
	X.add(x[0]); X.add(x[1]+1)
	Y.add(y[0]); Y.add(y[1]+1)
	Z.add(z[0]); Z.add(z[1]+1)
	commands.append((dict(on=1,off=0)[state], x, y, z))

X = sorted(list(X))
Y = sorted(list(Y))
Z = sorted(list(Z))

grid = np.zeros(shape=(len(X)-1, len(Y)-1, len(Z)-1), dtype="i8")

dx = X[1:] - np.array(X[:-1])
dy = Y[1:] - np.array(Y[:-1])
dz = Z[1:] - np.array(Z[:-1])
size = dx.reshape((-1,1,1)) * dy.reshape((1,-1,1)) * dz.reshape((1,1,-1))

	
for state, x, y, z in commands:
	i1,i2 = i = [X.index(w+d) for d,w in zip([0,1],x)]
	j1,j2 = j = [Y.index(w+d) for d,w in zip([0,1],y)]
	k1,k2 = k = [Z.index(w+d) for d,w in zip([0,1],z)]
	grid[i1:i2,j1:j2,k1:k2] = state

#i1,i2 = X.index(-50), X.index(51)
#j1,j2 = Y.index(-50), Y.index(51)
#k1,k2 = Z.index(-50), Z.index(51)
#grid = grid[i1:i2,j1:j2,k1:k2]
#size = size[i1:i2,j1:j2,k1:k2]

print(np.sum(grid))
grid *= size # this way we don't need allocate extra array
print(np.sum(grid))
