def source(fileName):
	source = ""
	with open(fileName) as f:
		source = f.read()
	return source

def sourceOfDefinitions(fileName):
	newSource = ""
	with open(fileName) as f:
		insideDefinition = False
		for line in f.readlines():
			if not line.strip():
				continue

			if (line.startswith(" ") or line.startswith("\t")) and insideDefinition:
				newSource += line
			elif line.startswith("def ") or line.startswith("class "):
				newSource += line
				insideDefinition = True
			elif line.startswith("import ") or line.startswith("from "):
				newSource += line
			else:
				insideDefinition = False

	return newSource