# -*- coding: utf-8 -*-

import Tkinter
import tkFileDialog
import multiprocessing
import time
import Process
import thread

class GUI:
    def __init__(self,so):
        self.window = Tkinter.Tk()
        self.so = so
        
        ## Llamadas
        Tkinter.Label(self.window, text="Numero telefono").pack()
        self.input_numero = Tkinter.Entry(self.window)
        self.input_numero.pack()
    
        ## Mensajes de texto
        Tkinter.Label(self.window, text="Mensaje de Texto").pack()
        self.input_mensaje = Tkinter.Entry(self.window)
        self.input_mensaje.pack()
        
        # Boton para llamar
        Tkinter.Button(self.window, text="LLamar a numero", command=self.llamar).pack()
        # Boton para cortar llamada
        Tkinter.Button(self.window, text="Terminar llamada", command=self.cortar).pack()
        # Boton para enviar mensaje
        Tkinter.Button(self.window, text="Enviar mensaje", command=self.enviar_mensaje).pack()
        # Bot�n para ver contactos
        Tkinter.Button(self.window, text="Ver contactos", command=self.ver_contactos).pack()
        # Boton para historial de llamadas
        Tkinter.Button(self.window, text="Ver historial llamadas", command=self.ver_contactos).pack()
        # Boton Ver mensajes
        Tkinter.Button(self.window, text="Ver mensajes", command=self.ver_contactos).pack()
        # Boton Ver procesos
        Tkinter.Button(self.window, text="Ver procesos", command=self.ver_contactos).pack()
        # Boton Ejecutar proceso
        Tkinter.Button(self.window, text="Ejecutar proceso", command=self.ver_contactos).pack()
        
        self.window.mainloop()
        
    def getNumero(self): # con este metodo se obtiene el valor del input para el telefono
        return self.input_numero.get()
    
    def getMensaje(self): # con este metodo se obtiene el valor del input para el mensaje
        return self.input_mensaje.get()
        
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
        
    def historial_llamadas(self):
        print 'Historial llamadas'
        
    def ver_mensajes(self):
        print 'Ver mensajes'
        
    def ver_procesos(self):
        print 'Ver Procesos'
        
    def ejecutar_proceso(self):
        print 'Ejecutar proceso'