class AdviceLevel:
	GOOD = 1
	MIXED = 2
	BAD = 3
	
class Advice(object):
	def __init__(self, adviceLevel, message):
		self._adviceLevel = adviceLevel
		self._message = message

	@property
	def adviceLevel(self):
		return self._adviceLevel
	
	@property
	def message(self):
		return self._message