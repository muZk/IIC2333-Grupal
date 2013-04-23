# -*- coding: utf-8 -*-
import Queue
import Process
import datetime
import time
from Memory import Memory 	

class Scheduler:
	def __init__(self):
		self.ready = Queue.PriorityQueue()
		self.running = None
		self.runningTime=0 #variable que registra el tiempo que lleva un programa en ejecucion
		self.IdCounter = 0
		self.incomingProcesses = list()
		self.time=0 #variable que registra el tiempo
		self.ejecutandose=True
	def getCurrentTime(self):
		return self.time

	def addProcess(self, process):
		self.ready.put((process.priority,process.pid))
		print 'Agregando ... {}'.format(process.toString())
		# Agregamos el proceso en memoria:
		Memory.saveProcess(process)
		
	def removeProcess(self,process):
		# Removemos un proceso
		Memory.removeProcess(process.pid)
		if self.running == process:
			self.running = None
			
	def loadProcessFromString(self,line,cor=True):
		atr = line.split(';')
		otros = list()
		for i in range(4, len(atr)):
			otros.append(atr[i])
		print otros
		if atr[2]=="1" or atr[2]=="6" or atr[2]=="8" or atr[2]=="9" or atr[2]=="10":
			cortar = cor
		else:
			cortar = False
		p = Process.Process(self.IdCounter,atr[0],atr[1],atr[2],atr[3],otros,cortar) 
		self.addProcess(p)
		#self.incomingProcesses.append(p)
		self.IdCounter=self.IdCounter+1
		#self.incomingProcesses.sort(key = lambda Process: -Process.execution_date) #ordeno por orden de llegada
		
	def loadProcesses(self):
		f = open("example.txt")
		lines = f.readlines()
		for line in lines:
			atr = line.split(';')
			otros = list()
			for i in range(4, len(atr)):
				otros.append(atr[i])
			p = Process.Process(self.IdCounter,atr[0],atr[1],atr[2],atr[3],otros,False)
			self.incomingProcesses.append(p)
			self.IdCounter=self.IdCounter+1
		self.incomingProcesses.sort(key = lambda Process: -Process.execution_date) #ordeno por orden de llegada
		
	def loadProcessFromMemory(self,pid):
		return Memory.loadProcess(pid)

	def readProcessFromMemory(self,pid):
		return Memory.readProcess(pid)

	def priorityScheduler(self):
		while self.ejecutandose:
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
			real_time_left = self.running.getTimeLeft() - self.runningTime;
			print 'checkIfFinished - pid '+str(self.running.pid)+' prioridad: '+str(self.running.priority)+' timeLeft: ' + str(real_time_left)
			if real_time_left<=0:
				self.registerLog()
				self.endProcess()

	def registerLog(self):
		if self.running.getProcessType()==1 or self.running.getProcessType()==2:#si es llamar o recibir llamada registrar en historial
			self.registerCalls()
		elif self.running.getProcessType()==3 or self.running.getProcessType()==4:#si es envio  o recibo de mensajes registrar en mensajes
			self.registerSMS()
		elif self.running.getProcessType()==5 or self.running.getProcessType()==7: #agregar contactos registrar en agenda
			self.addContact()
	
	def addContact(self):#guardo contactos formato Nombre;Numero
		f=open("Contactos.txt", "a")
		line=str(self.running.getOtros()[0])+";"+str(self.running.getOtros()[1])
		f.write(line)
			
	def registerSMS(self):#guardo SMS formato >(si es enviado)<(si es recibido);Numero;Fecha;Texto
		f=open("Mensajes.txt", "a")
		date = datetime.datetime.now()
		if self.running.getProcessType()==3:
			tipo = ">;"
		else:
			tipo = "<;"
		line = str(tipo)+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.getOtros()[1]) + "\n"
		f.write(line)
	
	def registerCalls(self):#guardo llamadas formato >(si es enviada)<(si es recibida);Numero;Fecha;Duracion
			f=open("Historial.txt", "a")
			date = datetime.datetime.now()
			if self.running.getProcessType()==1:
				tipo = ">;"
			else:
				tipo = "<;"
			line = str(tipo)+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.getOtros()[1]) + "\n"
			f.write(line)
	
	def exchange(self,process):
		print 'Expropiacion de '+self.running.toString()+' por '+process.toString();
		self.running.setTimeLeft(self.runningTime)
		self.runningTime=0
		paux = self.running
		self.running = process
		if self.running.cortable == True:
			print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)
		self.addProcess(paux)
	
	def endProcess(self):
		self.removeProcess(self.running) # removemos el proceso running de memoria
		self.runningTime = 0
		if not self.ready.empty():
			priority, pid = self.ready.get()
			self.running = self.loadProcessFromMemory(pid) # nuevo proceso entra
			if self.running.cortable == True:
				print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)
		else:
			print 'Scheduler.endProcess no hay procesos en cola ready'
	
	def endProcessByConsole(self,pid_ask):
		if pid_ask==self.running.pid:
			self.running.setTimeLeft(self.running.getTimeLeft())
		else :
			print "Su proceso está en cola o ya fue ejecutado"

	def checkPriorities(self):
			#ver si existe un proceso con mayor prioridad que running y si es necesario hacer los cambios
			if self.running is not None:#si se esta corriendo un proceso
				if not self.ready.empty():
					priority, pid = self.ready.get()
					if priority < self.running.getPriority():
						process = self.loadProcessFromMemory(pid)
						self.exchange(process)
					else:
						self.ready.put((priority,pid))
				else:
					print 'Scheduler.checkPriorities no hay procesos en cola ready'
			elif not self.ready.empty(): # self.running es null y tenemos procesos en cola
				priority, pid = self.ready.get()
				# cargamos desde Memoria
				self.running = self.loadProcessFromMemory(pid)
				if self.running.cortable == True:
					print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)
			
	def checkIncomingProc(self,t):
		while len(self.incomingProcesses)>0:
			#print 'checkIncomingProc '+str(self.incomingProcesses[-1].getExecutionDate())
			if self.incomingProcesses[-1].getExecutionDate()==t:
				self.addProcess(self.incomingProcesses.pop())
			else:
				break
	def showActiveProcess(self):
		# running
		print "------------------------------"
		if self.running is not None:
			print "Running:\npid = "+ str(self.running.pid) +" name = "+str(self.running.name)
		else:
			print "No hay procesos en running"	
		# ready
		if not self.ready.empty():
			print 'Ready:'
			for p in self.ready.queue:
				pid = p[1]
				process = self.readProcessFromMemory(pid)
				if process is not None: # por si las moscas!
					print "pid = "+str(process.pid)+" name = "+ process.name
		else:
			print "No hay procesos en Ready"
		print "------------------------------"

	def clock(self):
		self.time = self.time + 1
		if self.running is not None:
			self.runningTime = self.runningTime + 1					
		time.sleep(1)