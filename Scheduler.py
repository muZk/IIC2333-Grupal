# -*- coding: utf-8 -*-
import Queue
import Process
import datetime
import time
from IO import IO
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
		self.quantum=1
		self.tarea2=True
		#FINALEMNTE SOLO SE USO PROCESSIN[IO:PANTALLA] Y DADO QUE HABIAN ERRORES HICE SOLO UNA LISTA PARA LOS QUE USAN PANTALLA	
		# Cada IO tendra una lista de procesos que lo usan	
		"""self.processIn = []
		for io in range(0,5):
			self.processIn[io] = list()"""
		processInPantalla = []
			
		# Necesitamos una lista de procesos corriendo en paralelo
		self.pararellRunning = list()
		
		#Y otra para los que estan en waiting
		self.waiting = list()

	def getCurrentTime(self):
		return self.time

	def addProcess(self, process): #FALTA IMPLEMENTAR EXPROPIACIONES (Los if que aun tienen PASS)
		if self.tarea2==False:#tarea1
			self.ready.put((process.priority,process.pid))
			print 'Agregando ... {}'.format(process.toString())
			# Agregamos el proceso en memoria:
			Memory.saveProcess(process)
		else: #tarea2
			if process.getProcessType() in [1,2,3,4]:
				#Si es una llamada: (1 y 2)
				#	Entra solo si no hay algun proceso bloqueando audifonos y microfonos (1)
				#	Expropia a todos los procesos que esten usando los audifonos y/o microfonos (3,4,6,9 y 10)
				#Enviar y recibir mensajes: (3 y 4)
				#	Entra solo si no hay un proceso bloqueando los audifonos (1 y 2)
				#	No expropia
				entra = True #variable que es True si el proceso debiese entrar sin tomar en cuenta la prioridad
				for p in self.pararellRunning:  
					if not len(p.block)==0: #el proceso bloquea (es 1 o 2)
						entra = False
				if entra:
					if not len(process.block)==0: #si es 1 o 2			
						#se expropia a todos los procesos tipo 3,4,6,9 y 10 de pararellRunning
						self.exchange(process)
					#process entra a pararellRunning
					self.appendProcess(process)
				else: 
					#process pasa a waiting
					self.waiting.append(process)
			elif process.getProcessType()==7:
				#Entra a pararellRunning
				self.appendProcess(process)
			else: # 5,6,8,9,10
				#5 y 8: Entra solo si no hay un proceso que necesite la pantalla (6 y 9), a no ser de que tenga mayor prioridad. 
				#  Expropia en caso de tener mayor prioridad que 6 o 9 y que uno de estos este necesitando la pantalla
				#6 Entra solo si no hay un proceso que necesite la pantalla (9) a no ser de que tenga mayor prioridad, 
				#  Expropia a todos los que esten usando la pantalla o necesitandola
				#9 Entra solo si no hay un proceso que necesite la pantalla (6) a no ser de que tenga mayor prioridad, ni un proceso que bloquee los audifonos (1 y 2)
				#  Expropia a todos los que esten usando la pantalla o necesitandola
				#10 Entra solo si no hay un proceso que necesite la pantalla (6 y 9) a no ser de que tenga mayor prioridad,
				#  ni un proceso que bloquee los audifonos (1 y 2) No expropia
				entra = True
				verificarAudifonos = False
				if process.getProcessType()==9 or process.getProcessType()==10: #ver que no esten bloqueados los audifonos
					verificarAudifonos = True
				for p in self.pararellRunning:
					if p.needsIO():
						procesoQueNecesita = p
					if (verificarAudifonos) and (not len(p.block)==0): #si process es 9 o 10 y hay un proceso 1 o 2 en pararellRunning
						entra = False
				if entra:
					if process.getProcessType()==6 or process.getProcessType()==9:
						#expropia a todos los procesos tipo 5, 6, 8, 9 y 10 (solo si TODOS tienen menor prioridad) de pararellRunning
						expropiarCount = 0
						# hay procesos usando pantalla?
						if len(self.processInPantalla)>0:
							# verificar que tenga mejor prioridad que los que estan usando pantalla (o el que este necesitandola)
							for p in self.processInPantalla:
								if p.priority > process.priority:
									expropiarCount += 1
							# ver si es mejor que todos
							if expropiarCount == len(self.processInPantalla):
								# expropiamos todos los que usan pantalla
								usan = 'variable_que_decide_si_expropiar_a_los_que_usan_la_pantalla_o_a_el_que_la_necesita'
								self.exchange(process,usan)
						for p in self.pararellRunning: #Caso en el que hay que expropiar un proceso de parallel running que necesita la pantalla
							if p.getProcessType()==6 or p.getProcessType()==9:
								if p.priority > process.priority:
									#expropio a p
									self.exchange(process)
					else: #es 5,8,10 verificar su prioridad para ver si expropia a 6 o 9
						if procesoQueNecesita.priority > process.priority:
							#expropiar a  procesoQueNecesita
							self.exchange(process)	
					#process entra a pararellRunning
					self.appendProcess(process)
				else:
					#process pasa a waiting
					self.waiting.append(process)
								
	def appendProcess(self,process):#MODIFICADO
		# pasó todos los malditos filtros, ahora puede correr tranquilamente
		"""for io in process.use:
			self.processIn[io].append(process)"""
		if 'IO.PANTALLA' in process.use:
			self.processInPantalla.append(process)
		# agregamos a la running
		print 'Agregando ... {}'.format(process.toString())
		self.pararellRunning.append(process)
		if process.cortable == True:
			print "Para Cortar el proceso ingrese quit:"+str(process.pid)	
		# guardamos en memoria... aunque como lo tamos haciendo ya no es necesario
		Memory.saveProcess(process)
		
	def removeProcess(self,process): #MODIFICADO
		if self.tarea2 == False:
			# Removemos un proceso
			Memory.removeProcess(process.pid)
			if self.running == process:
				self.running = None
		else:#tarea2
			# no necesario pero igual
			Memory.removeProcess(process.pid)
			# remover de pararellRunning
			self.pararellRunning.remove(process)
			# remover de cada IO
			#for io in range(0,6):
			if process in self.processInPantalla:
				self.processInPantalla.remove(process)
				
	def loadProcessFromString(self,line,cor=True): #MODIFICADO
		atr = line.split(';')
		otros = list()
		for i in range(4, len(atr)):
			otros.append(atr[i])
		#print otros
		if atr[2]=="1" or atr[2]=="6" or atr[2]=="8" or atr[2]=="9" or atr[2]=="10":
			cortar = cor
		else:
			cortar = False
		p = Process.Process(self.IdCounter,atr[0],atr[1],atr[2],atr[3],otros,cortar) 
		if self.tarea2==False: #tarea1
			self.addProcess(p)
		else:#tarea2
			self.addProcess(p)
		#self.incomingProcesses.append(p)
		self.IdCounter=self.IdCounter+1
		#self.incomingProcesses.sort(key = lambda Process: -Process.execution_date) #ordeno por orden de llegada
		
	def loadProcesses(self):
		f = open("example.txt")
		lines = f.readlines()
		if len(lines)>0:
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

	def priorityScheduler(self): #MODIFICADO #Tarea 2 solo tendra un valor si se esta ejecutando la tarea 2 (ver Main)
		while self.ejecutandose:
			if self.tarea2 == False : #ejecutar tarea1
				#Revisar si llega alguien en el tiempo time y meterlo a la cola de prioridades
				self.checkIncomingProc(self.time) 
				#Si se acabo el proceso actual hacer cambios
				self.checkIfFinished()
				#Hacer cambios si existe un proceso con mayor prioridad a running
				self.checkPriorities()
				#Aumentar contador de segundos
				self.clock()
			else: #ejecutar Tarea 2
				print "checkIncomingProc"
				#Revisar si llega alguien en el tiempo time y meterlo a waiting o pararellRunning
				self.checkIncomingProc(self.time) 
				#Si se acabo algun proceso hacer cambios
				print "checkIfFinished"
				self.checkIfFinished()
				#Hacer cambios si existe un proceso en waiting que pueda entrar
				print "checkPriorities"
				self.checkPriorities() #IMPLEMENTAR, OJO QUE YA NO HAY READY, SINO QUE WAITING
				#Aumentar contador de segundos
				self.clock()
				
	def checkIfFinished(self):#MODIFICADO
		if self.tarea2 == False: #tarea1
			if self.running is not None:
				real_time_left = self.running.getTimeLeft() - self.runningTime;
				#print 'checkIfFinished - pid '+str(self.running.pid)+' prioridad: '+str(self.running.priority)+' timeLeft: ' + str(real_time_left)
				if real_time_left<=0:
					self.registerLog()
					self.endProcess()
		else: #tarea2
			if len(self.pararellRunning)>0:
				for running in self.pararellRunning:
					real_time_left = running.getTimeLeft() - self.runningTime;
					#print 'checkIfFinished - pid '+str(self.running.pid)+' prioridad: '+str(self.running.priority)+' timeLeft: ' + str(real_time_left)
					if real_time_left<=0:
						self.registerLog(running)
						self.endProcess(running)#Implementar

	def registerLog(self, p=None):#MODIFICADO
		if p == None: #registerLog para Tarea1
			if self.running.getProcessType()==1 or self.running.getProcessType()==2:#si es llamar o recibir llamada registrar en historial
				self.registerCalls()
			elif self.running.getProcessType()==3 or self.running.getProcessType()==4:#si es envio  o recibo de mensajes registrar en mensajes
				self.registerSMS()
			elif self.running.getProcessType()==5 or self.running.getProcessType()==7: #agregar contactos registrar en agenda
				self.addContact()
		else: #registerLog para Tarea2
			if p.getProcessType()==1 or p.getProcessType()==2:#si es llamar o recibir llamada registrar en historial
				self.registerCalls(p)
			elif p.getProcessType()==3 or p.getProcessType()==4:#si es envio  o recibo de mensajes registrar en mensajes
				self.registerSMS(p)
			elif p.getProcessType()==5 or p.getProcessType()==7: #agregar contactos registrar en agenda
				self.addContact(p)
				
	def addContact(self, p = None):#MODIFICADO
		#guardo contactos formato Nombre;Numero
		if p == None: #addContact para Tarea1
			f=open("Contactos.txt", "a")
			line=str(self.running.getOtros()[0])+";"+str(self.running.getOtros()[1])
			f.write(line)
		else: #addContact para Tarea2
			f=open("Contactos.txt", "a")
			line=str(p.getOtros()[0])+";"+str(p.getOtros()[1])
			f.write(line)
				
	def registerSMS(self, p = None):#MODIFICADO
		#guardo SMS formato >(si es enviado)<(si es recibido);Numero;Fecha;Texto
		if p == None: #registerSMS Tarea1
			f=open("Mensajes.txt", "a")
			date = datetime.datetime.now()
			if self.running.getProcessType()==3:
				tipo = ">;"
			else:
				tipo = "<;"
			line = str(tipo)+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.runningTime) + "\n"
			f.write(line)
		else: #registerSMS Tarea2
			f=open("Mensajes.txt", "a")
			date = datetime.datetime.now()
			if p.getProcessType()==3:
				tipo = ">;"
			else:
				tipo = "<;"
			line = str(tipo)+str(p.getOtros()[0]) + ";" + str(date) + ";" + str(p.runningTime) + "\n"
			f.write(line)

	def registerCalls(self, p = None):#MODIFICADO
		#guardo llamadas formato >(si es enviada)<(si es recibida);Numero;Fecha;Duracion
		if p == None: #registerCalls para Tarea1
			f=open("Historial.txt", "a")
			date = datetime.datetime.now()
			if self.running.getProcessType()==1:
				tipo = ">;"
			else:
				tipo = "<;"
			line = str(tipo)+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.runningTime) + "\n"
			f.write(line)
		else: #registerCalls para tarea 2
			f=open("Historial.txt", "a")
			date = datetime.datetime.now()
			if self.running.getProcessType()==1:
				tipo = ">;"
			else:
				tipo = "<;"
			line = str(tipo)+str(self.running.getOtros()[0]) + ";" + str(date) + ";" + str(self.running.runningTime) + "\n"
			f.write(line)
			
	def exchange(self,process, usan = None):#MODIFICADO
		if self.tarea2 == False: #Tarea1
			print 'Expropiacion de '+self.running.toString()+' por '+process.toString();
			self.running.setTimeLeft(self.runningTime)
			self.runningTime=0
			paux = self.running
			self.running = process
			if self.running.cortable == True:
				print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)
			self.addProcess(paux)
		else:
			if process.pid==1 or process.pid==2: #BLOQUEA
				for p in self.pararellRunning:
					if p.getProcessType() in [3,4,6,9,10]: #NECESITA
						print 'Expropiacion de '+p.toString()+' por '+process.toString()
						p.setTimeLeft(self.runningTime)
						self.runningTime=0
						paux = p
						self.addProcess(paux)
				#self.pararellRunning.append(process) ESTO YA ESTA HECHO EN ADDPROCESS	
			elif process.pid==6 or process.pid==9: #EXPROPIA AL QUE USA O NECESITA
				if not usan == None:
					for p in self.pararellRunning:
						if p.getProcessType in [5,8,10]: #USA
							print 'Expropiacion de '+p.toString()+' por '+process.toString()
							p.setTimeLeft(self.runningTime)
							self.runningTime=0
							paux = p
							self.addProcess(paux)
					#self.pararellRunning.append(process)
				else:
					for p in self.pararellRunning:
						if p.getProcessType in [6,9]:#NECESITA
							print 'Expropiacion de '+p.toString()+' por '+process.toString()
							p.setTimeLeft(self.runningTime)
							self.runningTime=0
							paux = p
							self.addProcess(paux)
			elif process.getProcessType() in [5,8,10]: #EXPROPIA A EL QUE NECESITA 
				for p in self.pararellRunning:
					if p.getProcessType in [6,9]: #NECESITA
						print 'Expropiacion de '+p.toString()+' por '+process.toString()
						p.setTimeLeft(self.runningTime)
						self.runningTime=0
						paux = p
						self.addProcess(paux)
			
	def endProcess(self, process = None): #MODIFICADO 
		if process == None: #Tarea1
			print 'Finalizando '+self.running.toString()
			self.removeProcess(self.running) # removemos el proceso running de memoria
			self.runningTime = 0
			if not self.ready.empty():
				priority, pid = self.ready.get()
				self.running = self.loadProcessFromMemory(pid) # nuevo proceso entra
				print "Ejecutando "+self.running.toString()+" t = "+str(self.time)
				if self.running.cortable == True:
					print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)
		else: #Tarea2
			for p in self.pararellRunning:
				if p.pid == process.pid:
					proceso = p
			print 'Finalizando '+proceso.toString()
			self.removeProcess(proceso) # removemos el proceso running de memoria
			self.runningTime = 0
			"""if not self.ready.empty():
				priority, pid = self.ready.get()
				self.running = self.loadProcessFromMemory(pid) # nuevo proceso entra
				print "Ejecutando "+self.running.toString()+" t = "+str(self.time)
				if self.running.cortable == True:
					print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)"""
		
	def endProcessByConsole(self,pid_ask): #MODIFICADO
		if self.tarea2 == False: #tarea1
			if pid_ask==self.running.pid:
				self.running.setTimeLeft(self.running.getTimeLeft())
				#print 'Finalizando proceso '+self.running.toString()
			else :
				print "Su proceso está en cola o ya fue ejecutado"
		else: #tarea2
			process = None
			for p in self.pararellRunning:
				if p.pid == pid_ask:
					process = p
			if process != None:
				process.setTimeLeft(process.getTimeLeft())
			else:
				print "Su proceso está en Waiting o ya fue ejecutado"

	def checkPriorities(self):#MODIFICADO
			if self.tarea2 == False: #tarea1
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
						pass
						#print 'No hay procesos en cola ready'
				elif not self.ready.empty(): # self.running es null y tenemos procesos en cola
					priority, pid = self.ready.get()
					# cargamos desde Memoria
					self.running = self.loadProcessFromMemory(pid)
					print 'Ejecutando '+self.running.toString() + ' t = ' + str(self.time)
					if self.running.cortable == True:
						print "Para Cortar el proceso ingrese quit:"+str(self.running.pid)
			else: #TAREA 2		
				i=0		
				k=len(self.waiting)
				while i<k:
					aux= self.waiting.pop(0)
					self.addProcess(aux)
					i=i+1
					
			
	def checkIncomingProc(self,t):#MODIFICADO

		if self.tarea2 == True:
			topop = list()

			for p in self.incomingProcesses:
				if p.getExecutionDate()==t:
					topop.append(p)

			for p in topop:
				self.addProcess(p)
				self.incomingProcesses.remove(p)

		else:
			while len(self.incomingProcesses)>0:
				#print 'checkIncomingProc '+str(self.incomingProcesses[-1].getExecutionDate())
				if self.incomingProcesses[-1].getExecutionDate()==t:
					if self.tarea2 == False: #tarea1
						self.addProcess(self.incomingProcesses.pop())
					else: #tarea2
						self.addProcess(self.incomingProcesses.pop())
					
	def showActiveProcess(self): #MODIFICADO
		if self.tarea2 == False: #tarea1
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
		else: #tarea2
			
			print "------------------------------"
			
			if len(self.pararellRunning)>0 :
				print "Procesos corriendo: (tiempo = "+str(self.time)
				for p in self.pararellRunning:
					print "pid = "+str(p.pid) + " name = "+str(p.name)
			
			else:
				print "No hay procesos corriendo"
				
			if len(self.waiting)>0 :
				print "Procesos en waiting:"
				for p in self.waiting:
					print "pid = "+str(p.pid) + " name = "+str(p.name)

		
	def clock(self):#MODIFICADO
		if self.tarea2 == False: #tarea1
			self.time = self.time + 1
			if self.running is not None:
				self.runningTime = self.runningTime + 1	
				self.running.runningTime = self.running.runningTime+1				
			time.sleep(1)
		else: #tarea2
			self.time = self.time + 1
			if len(self.pararellRunning)>0:
				for running in self.pararellRunning:
					self.runningTime = self.runningTime + 1	
					running.runningTime = running.runningTime+1				
			time.sleep(1)
			print "clock"