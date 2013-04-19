import Queue

class Scheduler:
	def __init__(self):
		self.ready = Queue.PriorityQueue()
		self.running = None

	def addProcess(self, process):
		self.ready.put((process.priority,process.pid))

	def nextProcess(self):
		""" Devuelve el proximo proceso a ejecutar	"""
		
		if not self.ready.empty(): # Si ready no esta vacío
			
			priority, pid = self.ready.get() # obtenemos datos del proceso con más prioridad
			
			if self.running is not None: # si hay un proceso en running
				if priority < self.running.priority: # comparar prioridades
					# nuevo proceso en running
					pass
				else:
					# se mantiene el proceso anterior en running, meter a ready lo que sacamos
					pass
			