import re

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

# source: http://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
def removeComments(source):
	source = re.sub(re.compile("\"\"\".*?\"\"\"",re.DOTALL), "", source) # remove all occurance streamed comments ("""COMMENT """) from string
	return re.sub(re.compile("#.*?\n"), "\n", source) # remove all occurance singleline comments (//COMMENT\n ) from string