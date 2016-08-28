import advice as a
import lib

def advice():
	source = lib.source(_fileName)
	usesSpaces = False
	usesTabs = False
	for line in source.split("\n"):
		for char in line:
			if char == " ":
				usesSpaces = True
			elif char == "\t":
				usesTabs = True
			else:
				break
		if usesSpaces and usesTabs:
			return a.Advice(a.AdviceLevel.BAD, "use of both tabs and spaces for indentation")

	if usesSpaces:
		return a.Advice(a.AdviceLevel.GOOD, "only using spaces for indentation")
	return a.Advice(a.AdviceLevel.GOOD, "only using tabs for indentation")