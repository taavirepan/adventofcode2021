import sys

ver = dict(x=0, y=0, z=0, w=0, inp=0)
val = dict(x00="0",y00="0",z00="0",w00="0")
for line in sys.stdin:
	op, *args = line.strip().split(" ")
	vargs = [f"{x}{ver[x]:02d}" if x in ver else x for x in args]
	oarg = f"{args[0]}{ver[args[0]]+1:02d}"
	vargs = [val.get(x, x) for x in vargs]
	
	if op == "mul" and vargs[0] == "1":
		val[oarg] = vargs[1]
	elif op == "mul" and vargs[1] == "1":
		val[oarg] = vargs[0]
	elif op == "mul" and vargs[0] == "0":
		val[oarg] = "0"
	elif op == "mul" and vargs[1] == "0":
		val[oarg] = "0"
	elif op == "mul":
		ap = lambda x: f"({x})" if " " in x else x
		val[oarg] = f"{ap(vargs[0])} * {ap(vargs[1])}"
	elif op == "add" and vargs[0] == "0":
		val[oarg] = vargs[1]
	elif op == "add" and vargs[1] == "0":
		val[oarg] = vargs[0]
	elif op == "add":
		val[oarg] = f"{vargs[0]} + {vargs[1]}"
	elif op == "div" and vargs[1] == "1":
		val[oarg] = vargs[0]
	elif op == "div" and vargs[1] == "26" and vargs[0].isdigit():
		assert int(vargs[0]) < 13
		val[oarg] = "0"
	elif op == "mod" and vargs[0] == "0":
		val[oarg] = "0"
	elif op == "mod" and vargs[0].isdigit() and vargs[1].isdigit():
		assert int(vargs[0]) < int(vargs[1])
		val[oarg] = vargs[0]
	elif op == "inp":
		ver["inp"] += 1
		val[oarg] = f"inp{ver['inp']:02d}"
	elif op == "eql" and vargs[1].startswith("inp"):
		val[oarg] = f"require({vargs[1]},{vargs[0]})"
	elif op == "eql" and vargs[1] == "0":
		print(f"{oarg} = {vargs[0]}")
	elif op == "eql" and vargs[1] == vargs[0]:
		val[oarg] = "1"
	elif op == "eql" and vargs[1] != vargs[0] and vargs[0].isdigit() and vargs[1].isdigit():
		val[oarg] = "0"
	else:
		print(f"{oarg} = {op}({', '.join(vargs)})")
	ver[args[0]] += 1

lz = f"z{ver['z']}"
print(f"return {val[lz]}")
