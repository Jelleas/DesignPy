from __future__ import division
import advice as a
import lib
import re

ADVICEMESSAGE = "possibly too few comments"

def advice():
	#print lib.source(_fileName)
	source = replaceStringsWithX(replaceCommentsWithHashes(lib.source(_fileName)))
	#print source

	nLines = 0
	nLinesOfComments = 0
	for line in source.split("\n"):
		nLines += 1
		if "#" in line:
			nLinesOfComments += 1

	if nLinesOfComments / nLines < 0.1:
		return a.Advice(a.AdviceLevel.UNSURE, ADVICEMESSAGE)

def replaceCommentsWithHashes(source):
	isNewLine = lambda c : c == "\n" or c == "\r\n" or c == "\r"
	replace = lambda m : "".join(["\n" if isNewLine(c) else "#" for c in str(m.group(0))])
	source = re.sub(re.compile("\"\"\".*?\"\"\"", re.DOTALL), replace, source)
	return re.sub(re.compile("#.*?\n"), replace, source)

def replaceStringsWithX(source):
	replace = lambda m : "\"" + "x" * (len(str(m.group(0))) - 2) + "\""
	source = re.sub(re.compile("\".*?\"", re.DOTALL), replace, source)
	return re.sub(re.compile("'.*?'", re.DOTALL), replace, source)