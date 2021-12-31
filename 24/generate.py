import sys
import re

def mod(a,b):
	return a%b

def div(a,b):
	return a//b

def get_code(vars):
	ret = ""
	for i in range(14):
		ret += str(vars.get(f"inp{i+1:02d}", "?"))
	return ret

def fill_inputs(expr, vars):
	for i in range(14):
		x = f"inp{i+1:02d}"
		if x in expr:
			for v in range(9):
				# v = 9-v
				v = 1+v
				yield from fill_inputs(expr.replace(x, str(v)), {**vars, x:v})
			return
	yield expr,vars

tests = 0
def solve(code, vars={}, line=1):
	global tests
	if len(code) == 0:
		return
	command0, *rest = code
	
	command = command0
	for k,v in vars.items():
		command = command.replace(k,str(v))
	
	m = re.match(r"(.\d+) = require\((.*),(.*)\)", command)
	if m:
		if not m[1][0].isalpha():
			print(line, command)
			print(line, command0)
			print(vars)
			exit()
		ok = False
		# assume not fullfilled
		# if line not in [8, 17, 22, 25, 31]:
		if line not in [8, 17, 22, 25, 31, 34]:
			ok = True
			solve(rest, {**vars, m[1]: 1}, line+1)
		# assume fulfilled
		for expr, nvars in fill_inputs(f"{m[2]} == {m[3]}", vars):
			if eval(expr):
				ok = True
				solve(rest, {**nvars, m[1]: 0}, line+1)
		if not ok and line in []:
			print(f"{line}: {command} failed ({get_code(vars)})")
			#print(f"{line}: {command} failed")
			#exit()
		return
	
	m = re.match(r"(.\d+) = (.*)", command)
	if m:
		for expr, nvars in fill_inputs(m[2], vars):
			res = eval(expr, {**vars, "mod": mod, "div": div})
			solve(rest, {**nvars, m[1]: res}, line+1)
		return
	
	m = re.match(r"return (.*)", command)
	if m:
		try:
			res = eval(m[1])
		except NameError as err:
			res = -1
		# print(get_code(vars), res)
		if res==0:
			print("ok:", get_code(vars))
			exit()
		tests += 1
		if tests>0 and tests%1000 == 0:
			print(f"{get_code(vars)}: {tests} tests done")
		# if tests >= 10000:
			# exit()
		return
		
	raise NotImplementedError(command)

code = [x.strip() for x in sys.stdin]
solve(code)
