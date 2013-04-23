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
        print 'Llamando a {}'.format(self.getNumero())
        process_string = '{};{};{};{};{}'.format('hacer_llamada',str(self.so.getCurrentTime()),'1','0',self.getNumero(),36000)
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
        while True:
            linea = f.readline()
            if not linea: break
            print linea

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
        process_string = "Ingrese el comando: "
        print process_string
        self.so.loadProcessFromString(process_string)