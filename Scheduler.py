import Queue

class Scheduler:
	def __init__(self):
		self.queue = Queue.PriorityQueue()

	def add(self, process):
		self.queue.put((process.priority,process.pid))
