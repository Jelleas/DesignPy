import advice as a
import lib

ADVICEMESSAGE = "consistent indentation"

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