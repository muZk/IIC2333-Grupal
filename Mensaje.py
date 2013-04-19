import time

class Mensaje(Process):
	
	def enviar_mensaje():

		print "Enviando a "+otros[0]+"..."
		time.sleep(len(otros[1]))
		print "Mensaje enviado"

	def recibir_mensaje():
		print "Mensaje entrante de "+otros[0]+"..."
		time.sleep(len(otros[1]))
		print "Mensaje recibido"