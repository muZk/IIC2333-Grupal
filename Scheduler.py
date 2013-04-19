import Queue
import Process
import datetime

class Scheduler:
	def __init__(self):
		self.ready = Queue.PriorityQueue()
		self.running = None
		self.runningTime=0 #variable que registra el tiempo que lleva un programa en ejecucion
		self.IdCounter = 0
		self.incomingProcesses = list()
		self.time=0 #variable que registra el tiempo

	def addProcess(self, process):
		self.ready.put((process.priority,process.pid))
		
		
	def loadProcesses(self):
		f = open("example.txt")
		lines = f.readlines()
		for line in lines:
			atr = line.split(';')
			otros = list()
			for i in range(4, len(atr)):
				otros.append(atr[i])
			p = Process.Process(self.IdCounter,atr[0],atr[1],atr[2],atr[3],otros)
			self.incomingProcesses.append(p)
			self.IdCounter=self.IdCounter+1
		self.incomingProcesses.sort(key = lambda Process: Process.execution_date) #ordeno por orden de llegada

	def priorityScheduler(self):
		while True:
			#Revisar si llega alguien en el tiempo time y meterlo a la cola de prioridades
			self.checkIncomingProc(self.time)
			#Si se acabo el proceso actual hacer cambios
			self.checkIfFinished()
			#Hacer cambios si existe un proceso con mayor prioridad a running
			self.checkPriorities()
			#Aumentar contador de segundos
			self.clock()
	
	def checkIfFinished(self):
		if self.running is not None:
			if self.running.getTimeLeft()==0:
				self.registerLog()
				self.endProcess()

	def registerLog(self):
		if self.running.getProcessType==1 or self.running.getProcessType==2:#si es llamar o recibir llamada registrar en historial
			self.registerCalls()
		elif self.running.getProcessType==3 or self.running.getProcessType==4:#si es envio  o recibo de mensajes registrar en mensajes
			self.registerSMS
		elif self.running.getProcessType==5 or self.running.getProcessType==7: #agregar contactos registrar en agenda
			self.addContact()
	
	def addContact(self):#guardo contactos formato Nombre;Numero
		f=open("Contactos.txt", "a")
		line=str(self.running.getOtros()[0])+";"+str(self.running.getOtros()[1])
		f.write(line)
			
	def registerSMS(self):#guardo SMS formato >(si es enviado)<(si es recibido);Numero;Fecha;Texto
		f=open("Mensajes.txt", "a")
		date = datetime.datetime.now()
		if self.running.getProcessType==3:
			tipo = ">;"
		else:
			tipo = "<;"
		line = str(tipo)+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.getOtros()[1]) + "\n"
		f.write(line)
	
	def registerCalls(self):#guardo llamadas formato >(si es enviada)<(si es recibida);Numero;Fecha;Duracion
			f=open("Historial.txt", "a")
			date = datetime.datetime.now()
			if self.running.getProcessType==1:
				tipo = ">;"
			else:
				tipo = "<;"
			line = str(tipo)+";"+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.getOtros()[1]) + "\n"
			f.write(line)
	
	def exchange(self,process):
		self.running.setTimeLeft(self.runningTime)
		self.runningTime=0
		paux = self.running
		self.running = process
		self.addProcess(paux)
	
	def endProcess(self):
		self.running = self.ready.get()
		self.runningTime = 0		
	
	def checkPriorities(self):
			#ver si existe un proceso con mayor prioridad que running y si es necesario hacer los cambios
			if self.running is not None:#si se esta corriendo un proceso
			
				if self.ready[0].getPriority()>self.running.getPriority():				
					self.exchange(self.ready.get())
			elif not self.ready.empty():
				self.running=self.ready.get()
			
	def checkIncomingProc(self,t):
		while self.incomingProcesses[0].getExecutionDate()==t:
					self.addProcess(self.incomingProcesses.pop())
		
	def clock(self):
		self.time = self.time + 1
		self.runningTime = self.runningTime + 1					
				