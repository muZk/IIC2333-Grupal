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
        return "(1) Llamar\n(2) Mandar mensaje\n(3) Ver contactos\n(4) Revisar historial\n(5) Ver procesos\n(6) Cargar archivo\n(7) Ejecutar proceso\n(8) Ver mensajes\n(9) Agregar contacto\n(10) Ver ubicación\n(11) Mandar ubicación\n(12) Jugar\n(13) Escuchar música\n(14) Proceso cualquiera\n(0) Salir\n"

    def mainloop(self):
        run = True
        while run:
            command = raw_input() # pedimos el input al usuario  
            if command == "1":
                self.llamar()
                cortar = raw_input ("Para Cortar presione q")
                if cortar == "q": 
                    self.cortar()
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
             elif command == "10":
                self.ver_ubicacion()
            elif command == "11":
                self.mandar_ubicacion()
            elif command == "12":
                self.jugar()
            elif command == "13":
                self.escuchar_musica()
            elif command=="14" 
                self.proceso_cualquiera()
                
            elif command == "0":
                pass
        
    def getNumero(self): # con este metodo se obtiene el valor del input para el telefono
        input_numero = raw_input('Ingrese el numero telefonico al cual desea llamar: ')
        return input_numero

    def getNumeroMensaje(self): # con este metodo se obtiene el valor del input para el telefono
        input_numero = raw_input('Ingrese el numero telefonico al cual desea enviar el mensaje: ')
        return input_numero
    
    
    def getNombreContacto(self): # con este metodo se obtiene el valor del input para el mensaje
        input_mensaje = raw_input('Ingrese el nombre del contacto que desea agregar: ')
        return input_mensaje
    
    def getNumeroContacto(self): # con este metodo se obtiene el valor del input para el mensaje
        input_mensaje = raw_input('Ingrese el numero telefonico que desea agregar: ')
        return input_mensaje
    
    def getMensaje(self): # con este metodo se obtiene el valor del input para el mensaje
        input_mensaje = raw_input('Ingrese el Mensaje de Texto: ')
        return input_mensaje
        
    def llamar(self):
        number = self.getNumero()
        print 'Llamando a: '+number
        process_string = '{};{};{};{};{};{}'.format('hacer_llamada',str(self.so.getCurrentTime()),'1','0',number,36000)
        print process_string
        self.so.loadProcessFromString(process_string)

    def cortar(self):
        print 'Cortando llamada'
        self.so.endProcess()

    def enviar_mensaje(self):
        process_string = '{};{};{};{};{};{}'.format('enviar_mensaje',str(self.so.getCurrentTime()),'3','2',self.getNumeroMensaje(),self.getMensaje())
        print process_string
        self.so.loadProcessFromString(process_string)
        
    def ver_contactos(self):
        print 'Viendo contactos'
        print 'Contactos'
        f=open("Contactos.txt", "r")
        numLinea = 0
        while True:
            linea = f.readline()
            if not linea: break
            numLinea=numLinea+1
            contact = linea.split(';')
            print str(numLinea)+") Nombre: "+contact[0]+"\t   Numero: "+contact[1]+"\n"

    def agregar_contacto(self):
        print 'Agregando contacto'
        process_string = '{};{};{};{};{};{}'.format('nuevo_contacto',str(self.so.getCurrentTime()),'5','6', self.getNombreContacto(), self.getNumeroContacto())
        print process_string
        self.so.loadProcessFromString(process_string)
        
    def historial_llamadas(self):
        print 'Historial llamadas'
        f=open("Historial.txt", "r")
        while True:
            linea = f.readline()
            if not linea: break
            print linea

    def ver_mensajes(self):
        print 'Ver mensajes'
        print 'Historial mensajes'
        f=open("Mensajes.txt", "r")
        while True:
            linea = f.readline()
            if not linea: break
            print linea
        
    def ver_procesos(self):
        print 'Ver Procesos'
        self.so.showActiveProcess()
        
    def ejecutar_proceso(self):
        print 'Ejecutar proceso'
        process_string = raw_input("Ingrese el comando: ")
        print process_string
        self.so.loadProcessFromString(process_string)

    def ver_ubicacion(self):
        pass
        
    def mandar_ubicacion(self):
        pass
    def jugar(self):
        pass
    def escuchar_musica(self):
        pass
    def proceso_cualquiera(self);
        pass
