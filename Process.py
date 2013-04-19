import math

class Process:
	def __init__(self,pid,name,execution_date,process_type,priority,otros):
		self.pid = pid
		self.name = name
		self.execution_date = int(execution_date)
		self.process_type = int(process_type)
		self.priority = int(priority)
		self.otros= otros
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
	
	def getPriority(self):
		return self.priority
	
	def setTimeLeft(self,time):#ojo, el metodo no setea el tiempo que queda sino que actualiza el tiempo que le queda segun cuanto tiempo estuvo en running por ultima vez antes de ser expropiado
		self.timeLeft = self.timeLeft - int(time)
	
	def getTimeLeft(self):
		return self.timeLeft
	
	def getOtros(self):
		return self.otros
	
	def getProccesType(self):
		return self.process_type
		
	def getExecutionDate(self):
		return self.execution_date