# For instructions on how to use, please refer to my GitHub: 

from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
	data = open(filename, "r").read()
	data += "~EOF~"
	return data

def lex(filecontents):
	roots = []
	tok = ""
	state = 0
	string = ""
	expr = ""
	n = 0
	isexpr = 0
	varstarted = 0
	var = ""
	commentstarted = 0
	comment = ""
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char
		if tok == " ":
			if state == 0:
				tok = ""
			else:
				tok = " "
		elif tok == "\n" or tok == "~EOF~":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varstarted = 0
			tok = ""
		elif tok == "<":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("LESSTHAN")
			tok = ""
		elif tok == ">":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("MORETHAN")
			tok = ""
		elif tok == "!":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("NOT")
			tok = ""
		elif tok == "=" and state == 0:
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				varstarted = 0
			if tokens[-1] == "EQUALS":
				tokens[-1] = "EQEQ"
			elif tokens[-1] == "NOT":
				tokens[-1] = "NOTEQUAL"
			elif tokens[-1] == "LESSTHAN":
				tokens[-1] = "LESSOREQUAL"
			elif tokens[-1] == "MORETHAN":
				tokens[-1] = "MOREOREQUAL"
			else:
				tokens.append("EQUALS")
			tok = ""
		#vars
		elif tok == "@" and state == 0:
			varstarted = 1
			var += tok
			tok = ""
		elif varstarted == 1:
			if tok == "<" or tok == ">" and state == 0:
				if var != "":
					tokens.append("VAR:" + var)
					var = ""
					varstarted = 0
				var += tok
				tok = ""
			var += tok
			tok = ""
		#comments
		elif tok == "#":
			commentstarted = 1
			comment += tok
			tok = ""
		elif commentstarted == 1:
			if tok == ";":
				tokens.append("COMMENT:" + comment)
				comment = ""
				commentstarted = 0
			comment += tok
			tok = ""
		elif tok == "OUT":
			tokens.append("OUT")
			tok = ""
		elif tok == "IN":
			tokens.append("IN")
			tok = ""
		elif tok == "ENDIF":
			tokens.append("ENDIF")
			tok = ""
		elif tok == "IF":
			tokens.append("IF")
			tok = ""		
		elif tok == "THEN":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("THEN")
			tok = ""
		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
			expr += tok
			tok = ""
		elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
			if tok == "/" or tok == "*":
				roots.append(tok)
			isexpr = 1
			expr += tok
			tok = ""
		elif tok == "\"" or tok == " \"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1:
			string += tok
			tok = ""
	return [x for x in tokens if not "COMMENT" in x]
	

def evalExpression(expr):
	return eval(expr)
	
def doOUT(toOUT):
	if toOUT[0:6] == "STRING":
		toOUT = toOUT[8:]
		toOUT = toOUT[:-1]
	elif toOUT[0:3] == "NUM":
		toOUT = toOUT[4:]
	elif toOUT[0:4] == "EXPR":
		toOUT = evalExpression(toOUT[5:])
	print(toOUT)

def doASSIGN(varname, varvalue):
	symbols[varname[4:]] = varvalue

def getVARIABLE(varname):
	varname = varname[4:]
	if varname in symbols:
		return symbols[varname]
	else:
		return "ERROR: UNDEFINED VARIABLE"
		exit()

def getIN(string, varname):
	i = raw_input(string[1:-1] + " ")
	symbols[varname] = "STRING:\"" + i + "\""

def doIF_FALSE(tokens):
	ii = 0
	for token in tokens:
		if token == "IF":
			ii = 1
		elif token == "ENDIF":
			ii += 1
			break
		else:
			ii += 1
	print tokens[ii:]
	return ii

def parse(toks):
	i = 0
	while(i < len(toks)):
		if toks[i] == "ENDIF":
			
			i += 1
		elif toks[i] + " " + toks[i+1][0:6] == "OUT STRING" or toks[i] + " " + toks[i+1][0:3] == "OUT NUM" or toks[i] + " " + toks[i+1][0:4] == "OUT EXPR" or toks[i] + " " + toks[i+1][0:3] == "OUT VAR":
			if toks[i+1][0:6] == "STRING":
				doOUT(toks[i+1])
			elif toks[i+1][0:3] == "NUM":
				doOUT(toks[i+1])
			elif toks[i+1][0:4] == "EXPR":
				doOUT(toks[i+1])
			elif toks[i+1][0:3] == "VAR":
				doOUT(getVARIABLE(toks[i+1]))
			i += 2
		elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][:3] + " " + toks[i+1] + " " + toks[i+2][:3] == "VAR EQUALS NUM" or toks[i][:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
			if toks[i+2][0:6] == "STRING":
				doASSIGN(toks[i], toks[i+2])
			elif toks[i+2][0:3] == "NUM":
				doASSIGN(toks[i], toks[i+2])
			elif toks[i+2][0:4] == "EXPR":
				doASSIGN(toks[i], "NUM:" + str(evalExpression(toks[i+2][5:])))
			elif toks[i+2][0:3] == "VAR":
				doASSIGN(toks[i], getVARIABLE(toks[i+2]))
			i += 3
		elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "IN STRING VAR":
			getIN(toks[i+1][7:], toks[i+2][4:])
			i += 3
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM EQEQ NUM THEN":
			if toks[i+1][4:] == toks[i+3][4:]:
				i += 5
			else:
				i = doIF_FALSE(toks[i:])
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM LESSTHAN NUM THEN":
			if toks[i+1][4:] < toks[i+3][4:]:
				i += 5
			else:
				i = doIF_FALSE(toks[i:])
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM MORETHAN NUM THEN":
			if toks[i+1][4:] > toks[i+3][4:]:
				i += 5
			else:
				i = doIF_FALSE(toks[i:])
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM LESSOREQUAL NUM THEN":
			if toks[i+1][4:] <= toks[i+3][4:]:
				i += 5
			else:
				i = doIF_FALSE(toks[i:])
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM MOREOREQUAL NUM THEN":
			if toks[i+1][4:] >= toks[i+3][4:]:
				i += 5
			else:
				i = doIF_FALSE(toks[i:])
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM NOTEQUAL NUM THEN":
			if toks[i+1][4:] != toks[i+3][4:]:
				i += 5
			else:
				i = doIF_FALSE(toks[i:])

def run():
	data = open_file(argv[1])
	toks = lex(data)
	parse(toks)

run()

