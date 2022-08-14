
class Thread_:
	def __init__(self):
		self.convert = True


	def stop(self):
		self.convert = False

	def get_convert(self):
		return self.convert
