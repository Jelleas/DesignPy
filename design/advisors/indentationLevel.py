import advice as a
import lib
import statemachine as sm

ADVICEMESSAGE = "consistent indentation"

_indentationLevel = 0
_indentationStep = ""

def advice():
	source = lib.removeComments(lib.source(_fileName))
	setIndentationStep(getIndentationStep(source))

	defaultState = sm.State("default", lambda line : "unexpected error occured at: {}".format(line.strip()))
	mustMatchIndentation = sm.State("must match indentation", lambda line : "incorrect indentation at: {}".format(line.strip()))
	backslash = sm.State("backslash", lambda line : "unexpected error occured at: {}".format(line.strip()))

	defaultState.addTransition(\
		mustMatchIndentation,\
		lambda line : endsWithDoubleDot(line),\
		action = lambda line : setIndentationLevel(line) and incrementIndentationLevel())
	defaultState.addTransition(\
		backslash,\
		endsWithBackslash)
	defaultState.addTransition(\
		defaultState,\
		lambda line : (getIndentationLevel(line) <= _indentationLevel),\
		action = setIndentationLevel)

	mustMatchIndentation.addTransition(\
		mustMatchIndentation,\
		lambda line : endsWithDoubleDot(line) and matchesIndentationLevel(line),\
		action = lambda line : incrementIndentationLevel())
	mustMatchIndentation.addTransition(\
		backslash,\
		lambda line : endsWithBackslash(line) and matchesIndentationLevel(line))
	mustMatchIndentation.addTransition(\
		defaultState,\
		lambda line : matchesIndentationLevel(line),\
		action = setIndentationLevel)

	backslash.addTransition(\
		mustMatchIndentation,\
		lambda line : endsWithDoubleDot(line),\
		action = lambda line : incrementIndentationLevel())
	backslash.addTransition(\
		backslash,\
		endsWithBackslash)
	backslash.addTransition(\
		defaultState,\
		lambda line : True)

	success, message = sm.StateMachine(defaultState).run((line for line in source.split("\n") if len(line.strip()) != 0))
	if success:
		return a.Advice(a.AdviceLevel.GOOD, ADVICEMESSAGE)
	return a.Advice(a.AdviceLevel.BAD, ADVICEMESSAGE, message)

def getIndentationStep(source):
	nextLineIndented = False
	for line in source.split("\n"):
		if nextLineIndented:
			indentationStep = ""
			for char in line:
				if char == " " or char == "\t":
					indentationStep += char
				else:
					return indentationStep

		if line.strip().endswith(":"):
			nextLineIndented = True

	return ""

def endsWithBackslash(line):
	return line.strip().endswith("\\")

def endsWithDoubleDot(line):
	return line.strip().endswith(":")

def matchesIndentationLevel(line):
	return getIndentationLevel(line) == _indentationLevel

def ifMatchesThenSetIndentationLevel(line):
	if matchesIndentationLevel(line):
		return setIndentationLevel(line)
	return False

def setIndentationStep(indentationStep):
	global _indentationStep
	_indentationStep = indentationStep
	return True

def setIndentationLevel(line):
	global _indentationLevel
	_indentationLevel = getIndentationLevel(line)
	return True

def incrementIndentationLevel():
	global _indentationLevel
	_indentationLevel += 1
	return True

def getIndentationLevel(line):
	indentationLevel = 0
	while line.startswith(_indentationStep):
		indentationLevel += 1
		line = line[len(_indentationStep):]
	return indentationLevel


"""
def advice():
	source = lib.removeComments(lib.source(_fileName))

	indentationStep = getIndentationStep(source)
	indentationLevel = 0
	mustMatchIndentation = False
	for line in (line for line in source.split("\n") if len(line.strip()) != 0):
		if mustMatchIndentation and not line.startswith(indentationStep * indentationLevel):
			return a.Advice(a.AdviceLevel.BAD, ADVICEMESSAGE, "on line: {}".format(line.strip()))
		elif not line.startswith(indentationStep * indentationLevel):
			indentationLevel = 0
			tempLine = line
			while tempLine.startswith(indentationStep):
				indentationLevel += 1
				tempLine = tempLine[len(indentationStep):]
		else:
			tempLine = line[len(indentationStep * indentationLevel):]
			if tempLine.startswith(" ") or tempLine.startswith("\t"):
				return a.Advice(a.AdviceLevel.BAD, ADVICEMESSAGE, "on line: {}".format(line.strip()))

		if line.strip().endswith(":"):
			indentationLevel += 1
			mustMatchIndentation = True
		else:
			mustMatchIndentation = False

	return a.Advice(a.AdviceLevel.GOOD, ADVICEMESSAGE)
"""