import advice as a
import lib

ADVICEMESSAGE = "blank lines before all comments"

class StateException(Exception):
	pass

class StateMachine(object):
	def __init__(self, start):
		self._start = start

	def run(self, lineGen):
		state = self._start
		for line in lineGen:
			try:
				state = state.next(line)
			except StateException as e:
				return False, str(e)
		return True, ""

class State(object):
	def __init__(self, name, errorMessageCreator):
		self._name = name
		self._errorMessageCreator = errorMessageCreator
		self._transitions = []

	def addTransition(self, nextState, condition):
		self._transitions.append((nextState, condition))

	def next(self, line):
		for state, condition in self._transitions:
			if condition(line):
				return state
		raise StateException(self._errorMessageCreator(line))

def advice():
	mustBeBlank = State("single line comment", lambda line : "expected a blank line, but got: {}".format(line.strip()))
	multiLine = State("multi line comment", lambda line : "expected a blank line, but got: {}".format(line.strip()))
	noComment = State("no comment", lambda line : "unexpected error at: {}".format(line.strip()))

	noComment.addTransition(mustBeBlank, lambda line : isSingleLineComment(line))
	noComment.addTransition(multiLine, lambda line : containsMultiLineComment(line))
	noComment.addTransition(noComment, lambda line : True)

	mustBeBlank.addTransition(noComment, lambda line : isBlank(line))
	mustBeBlank.addTransition(multiLine, lambda line : containsMultiLineComment(line))
	mustBeBlank.addTransition(mustBeBlank, lambda line : isSingleLineComment(line))
	
	multiLine.addTransition(mustBeBlank, lambda line : containsMultiLineComment(line))
	multiLine.addTransition(multiLine, lambda line : True)

	success, message = StateMachine(noComment).run(lib.source(_fileName).split("\n")[::-1])
	if success:
		return a.Advice(a.AdviceLevel.GOOD, ADVICEMESSAGE)
	return a.Advice(a.AdviceLevel.BAD, ADVICEMESSAGE, message)

def isBlank(line):
	return len(line.strip()) == 0

def isSingleLineComment(line):
	return line.strip().startswith("#") or line.count("\"\"\"") >= 2

def containsMultiLineComment(line):
	return line.count("\"\"\"") >= 1