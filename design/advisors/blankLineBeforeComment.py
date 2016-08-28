import advice as a
import lib
import statemachine as sm

ADVICEMESSAGE = "blank lines before all comments"

def advice():
	mustBeBlank = sm.State("single line comment", lambda line : "expected a blank line, but got: {}".format(line.strip()))
	multiLine = sm.State("multi line comment", lambda line : "expected a blank line, but got: {}".format(line.strip()))
	noComment = sm.State("no comment", lambda line : "unexpected error at: {}".format(line.strip()))

	noComment.addTransition(mustBeBlank, lambda line : isSingleLineComment(line))
	noComment.addTransition(multiLine, lambda line : containsMultiLineComment(line))
	noComment.addTransition(noComment, lambda line : True)

	mustBeBlank.addTransition(noComment, lambda line : isBlank(line))
	mustBeBlank.addTransition(multiLine, lambda line : containsMultiLineComment(line))
	mustBeBlank.addTransition(mustBeBlank, lambda line : isSingleLineComment(line))
	
	multiLine.addTransition(mustBeBlank, lambda line : containsMultiLineComment(line))
	multiLine.addTransition(multiLine, lambda line : True)

	success, message = sm.StateMachine(noComment).run(lib.source(_fileName).split("\n")[::-1])
	if success:
		return a.Advice(a.AdviceLevel.GOOD, ADVICEMESSAGE)
	return a.Advice(a.AdviceLevel.BAD, ADVICEMESSAGE, message)

def isBlank(line):
	return len(line.strip()) == 0

def isSingleLineComment(line):
	return line.strip().startswith("#") or line.count("\"\"\"") >= 2

def containsMultiLineComment(line):
	return line.count("\"\"\"") >= 1