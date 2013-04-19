import time
import Process

class Llamada(Process):
	
	def realizar_llamada(self):

		print "Llamando a "+self.otros[0]+"..."
		time.sleep(self.otros[1])
		print "Llamada finalizada"

	def recibir_llamada(self):

		print "Llamada entrante de "+self.otros[0]+"..."
		time.sleep(self.otros[1])
		print "Llamada finalizada"

