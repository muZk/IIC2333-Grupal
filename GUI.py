# -*- coding: utf-8 -*-

import Tkinter
import tkFileDialog
import multiprocessing
import time
import Process
import thread

class GUI:
    def __init__(self,so):
        
        self.so = so
        print self.opciones()
        self.mainloop()
        
    def opciones(self):
        return "(1) Llamar\n(2) Mandar mensaje\n(3) Ver contactos\n(4) Revisar historial\n(5) Ver procesos\n(6) Cargar archivo\n(7) Ejecutar proceso\n(8) Ver mensajes\n(9) Agregar contacto\n(0) Salir\n"

    def mainloop(self):
        run = True
        while run:
            command = raw_input() # pedimos el input al usuario  
            if command == "1":
                self.llamar()
            elif command == "2":
                self.enviar_mensaje()
            elif command == "3":
                self.ver_contactos()
            elif command == "4":
                self.historial_llamadas()
            elif command == "5":
                self.ver_procesos()
            elif command == "6":
                pass
            elif command == "7":
                self.ejecutar_proceso()
            elif command == "8":
                self.ver_mensajes()
            elif command == "9":
                self.agregar_contacto()
            elif command == "0":
                pass
        
    def getNumero(self): # con este metodo se obtiene el valor del input para el telefono
        input_numero = raw_input('Ingrese el número Telefónico al cual desea llamar')
        return input_numero
    
    def getMensaje(self): # con este metodo se obtiene el valor del input para el mensaje
        input_mensaje = raw_input('Ingrese el Mensaje de Texto')
        return input_mensaje
        
    def llamar(self):
        print 'Llamando a {}'.format(self.getNumero())
        
    def cortar(self):
        print 'Cortando llamada'
        
    def enviar_mensaje(self):
        process_string = '{};{};{};{};{};{}'.format('enviar_mensaje',str(self.so.getCurrentTime()),'3','2',self.getNumero(),self.getMensaje())
        print process_string
        self.so.loadProcessFromString(process_string)
        
    def ver_contactos(self):
        print 'Viendo contactos'
        
    def agregar_contacto(self):
        print 'Agregando contacto'
        
    def historial_llamadas(self):
        print 'Historial llamadas'
        
    def ver_mensajes(self):
        print 'Ver mensajes'
        
    def ver_procesos(self):
        print 'Ver Procesos'
        
    def ejecutar_proceso(self):
        print 'Ejecutar proceso'