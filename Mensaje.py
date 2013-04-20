import time

class Mensaje(Process):
	
	def enviar_mensaje(self):

		print "Enviando a "+otros[0]+"..."
		time.sleep(len(otros[1])*20/1000)
		print "Mensaje enviado"

	def recibir_mensaje(self):
		print "Mensaje entrante de "+otros[0]+"..."
		time.sleep(len(otros[1])*20/1000)
		print "Mensaje recibido"


