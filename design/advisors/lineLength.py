import advice as a
import lib

MAXLINELENGTH = 80

def advice():
	source = lib.source(_fileName)
	for line in source.split("\n"):
		if len(line) > MAXLINELENGTH:
			return a.Advice(a.AdviceLevel.BAD, "code contains lines longer than {} characters".format(MAXLINELENGTH))
	return a.Advice(a.AdviceLevel.GOOD, "all lines in the code are not longer than {} characters".format(MAXLINELENGTH))