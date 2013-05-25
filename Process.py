# -*- coding: utf-8 -*-

import math
import time
from IO import IO

class Process:
	def __init__(self,pid,name,execution_date,process_type,priority,otros,cortable):
		self.pid = pid
		self.name = name
		self.execution_date = int(execution_date)
		self.process_type = int(process_type)
		self.priority = int(priority)
		self.otros= otros
		self.runningTime = 0 # para fixear las cosas con duracion infinita
		#se define el tiempo de ejecucion segun el tipo de proceso
		if self.process_type==1 or self.process_type==2:#si es llamar o recibir llamada
			self.execution_time=int(self.otros[1])
		elif self.process_type==3 or self.process_type==4:#si es envio  o recibo de mensajes
			self.execution_time=math.ceil(0.02*len(self.otros[1]))#cantidad de letras * 0,02 redondeado hacia arriba
		#Agregar contactos no usa tiempo?? Por defecto asumimos que se demora 1
		elif self.process_type==5 or self.process_type==7: #agregar contactos o enviar ubicacion
			self.execution_time=2
		else:
			self.execution_time=int(self.otros[0])
		#se crea la variable que guarda el tiempo restante para que el proceso termine de ejecutarse
		self.timeLeft = self.execution_time
		self.cortable=cortable
		
		# Definimos lo que bloquea el proceso
		self.block = list()
		self.need = None
		self.use = list()
		
		"  Las definiciones salen en la tabla de la pagina 3 de la tarea "
		
		# PANTALLA
		if self.process_type in [1,2,5,8,10]:
			self.use.append(IO.PANTALLA)
			
		# AUDIFONO
		if self.process_type in [3,4,6,9,10]:
			self.use.append(IO.AUDIFONO)
			
		# MICROFONO
		if self.process_type in [6] :
			self.use.append(IO.MICROFONO)
		
		# GPS
		if self.process_type in [6,7,8,9]:
			self.use.append(IO.GPS)
		
		# ENVIAR
		if self.process_type in [1,2,3,4,6,7,9]:
			self.use.append(IO.ENVIAR)
		
		# RECIBIR
		if self.process_type in [1,2,3,4,6,9]:
			self.use.append(IO.RECIBIR)
		
		# ================== BLOQUEAR ===================
		
		# AUDIFONO y MICROFONO
		if self.process_type in [1,2]:
			self.block.append(IO.AUDIFONO)
			self.block.append(IO.MICROFONO)
			
		# ================== NECESITAR ===================
		
		# PANTALLA
		if self.process_type in [6,9]:
			self.need = IO.PANTALLA
	
	def getPriority(self):
		return self.priority
	
	def setTimeLeft(self,time):#ojo, el metodo no setea el tiempo que queda sino que actualiza el tiempo que le queda segun cuanto tiempo estuvo en running por ultima vez antes de ser expropiado
		self.timeLeft = self.timeLeft - int(time)
	
	def getTimeLeft(self):
		return self.timeLeft
	
	def getOtros(self):
		return self.otros
	
	def getProcessType(self):
		return self.process_type
		
	def getExecutionDate(self):
		return self.execution_date

	def toString(self):
		return '(name={},pid={},priority={},type={})'.format(self.name,str(self.pid),str(self.priority),str(self.process_type))

	def needsIO(self):
		return self.need != None
	
