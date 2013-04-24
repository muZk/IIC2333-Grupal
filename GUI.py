# -*- coding: utf-8 -*-

class GUI:
    def __init__(self,so):
        
        self.so = so
        print self.opciones()
        self.mainloop()
        
    def opciones(self):
        return "(1) Llamar\n(2) Mandar mensaje\n(3) Ver contactos\n(4) Revisar historial\n(5) Ver procesos\n(6) Ejecutar proceso\n(7) Ver mensajes\n(8) Agregar contacto\n(9) Ver ubicación\n(10) Mandar ubicación\n(11) Jugar\n(12) Escuchar música\n(13) Proceso cualquiera\n(0) Salir\n"

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
                self.ejecutar_proceso()
            elif command == "7":
                self.ver_mensajes()
            elif command == "8":
                self.agregar_contacto()
            elif command == "9":
                self.ver_ubicacion()
            elif command == "10":
                self.mandar_ubicacion()
            elif command == "11":
                self.jugar()
            elif command == "12":
                self.escuchar_musica()
            elif command == "13":
                self.proceso_cualquiera()
            elif command == "0":
                self.so.ejecutandose=False
                run=False
                print "Chao!"
            else:
                # cortar proceso, ifs para que no se caiga cuando ingresan cualquier cosa
                if len(command)>5: 
                    if command[:5] == 'quit:':
                        id = command.split(':')[1]
                        self.so.endProcessByConsole(int(id))
                        
        
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
        #print 'Llamando a: '+number
        process_string = '{};{};{};{};{};{}'.format('hacer_llamada',str(self.so.getCurrentTime()),'1','0',number,36000)
        #print process_string
        self.so.loadProcessFromString(process_string)

    def enviar_mensaje(self):
        process_string = '{};{};{};{};{};{}'.format('enviar_mensaje',str(self.so.getCurrentTime()),'3','2',self.getNumeroMensaje(),self.getMensaje())
        #print process_string
        self.so.loadProcessFromString(process_string)
        
    def ver_contactos(self):
        #print 'Viendo contactos'
        #print 'Contactos'
        f=open("Contactos.txt", "r")
        numLinea = 0
        while True:
            linea = f.readline()
            if not linea: break
            numLinea=numLinea+1
            contact = linea.split(';')
            print str(numLinea)+") Nombre: "+contact[0]+"\t   Numero: "+contact[1]+"\n"
        numero = str(raw_input("a) Para volver al menu principal presione q\nb) Si desea llamar a un contacto presione el numero del contacto en la agenda recien desplegada\n(No el numero de telefono, sino que el de la ubicacion en la lista)\n"))
        if numero == 'q':
            pass
        else:
            f2=open("Contactos.txt", "r")
            numLinea2=0
            try:
                while True:
                    linea2=f2.readline()
                    if not linea2: break
                    numLinea2=numLinea2+1
                    if numLinea2==int(numero):
                        contacto = linea2.split(';')
                        #print 'Llamando a: '+contacto[0]
                        process_string = '{};{};{};{};{};{}'.format('hacer_llamada',str(self.so.getCurrentTime()),'1','0',contacto[1],36000)
                        #print process_string
                        self.so.loadProcessFromString(process_string)
                        break
            except:
                print "Error al ingresar datos, vuelva a intentar"

    def agregar_contacto(self):
        #print 'Agregando contacto'
        process_string = '{};{};{};{};{};{}'.format('nuevo_contacto',str(self.so.getCurrentTime()),'5','6', self.getNombreContacto(), self.getNumeroContacto())
        #print process_string
        self.so.loadProcessFromString(process_string)
        
    def historial_llamadas(self):
        print 'Historial llamadas\n'
        f=open("Historial.txt", "r")
        while True:
            linea = f.readline()
            if not linea: break
            llamada = linea.split(';')
            tipo = " Realizada"
            if llamada[0] == "<": tipo=" Recibida"
            if len(llamada)>1:
                print "Llamada"+tipo+"\t Numero: "+llamada[1]+"\t Fecha: "+llamada[2]+"\t Duracion: "+llamada[3]+"\n"

    def ver_mensajes(self):
        print 'Ver mensajes\n'
        print 'Historial mensajes'
        f=open("Mensajes.txt", "r")
        while True:
            linea = f.readline()
            if not linea: break
            mensaje = linea.split(';')
            tipo = " Enviado"
            if mensaje[0] == "<": tipo=" Recibido"
            if len(mensaje)>1:
                print "Mensaje"+tipo+"\t Numero: "+mensaje[1]+"\t Fecha: "+mensaje[2]+"\t Texto: "+mensaje[3]+"\n"

        
    def ver_procesos(self):
        #print 'Ver Procesos'
        self.so.showActiveProcess()
        
    def ejecutar_proceso(self):
        #print 'Ejecutar proceso'
        process_string = raw_input("Ingrese el comando: ")
        #print process_string
        self.so.loadProcessFromString(process_string,False)

    def ver_ubicacion(self):
        #print 'Viendo ubicacion: '
        process_string = '{};{};{};{};{}'.format('ver_ubicacion',str(self.so.getCurrentTime()),'8','8',36000)
        #print process_string
        self.so.loadProcessFromString(process_string)
        
    def mandar_ubicacion(self):
        #demora 2
        #print 'Mandando ubicacion: '
        process_string = '{};{};{};{};{}'.format('mandar_ubicacion',str(self.so.getCurrentTime()),'7','8',2)
        #print process_string
        self.so.loadProcessFromString(process_string)
        
    def jugar(self):
        nombre = raw_input("¿Que desea jugar?")
        #print 'Jugando: '
        process_string = '{};{};{};{};{}'.format(nombre,str(self.so.getCurrentTime()),'9','8',36000)
        #print process_string
        self.so.loadProcessFromString(process_string)
        
    def escuchar_musica(self):
        #print 'musica: '
        process_string = '{};{};{};{};{}'.format('escuchar_musica',str(self.so.getCurrentTime()),'10','8',36000)
        #print process_string
        self.so.loadProcessFromString(process_string)
        
    def proceso_cualquiera(self):
        nombre = raw_input("¿Que desea ejecutar?")
        #print 'procesando cualquera: '
        process_string = '{};{};{};{};{}'.format(nombre,str(self.so.getCurrentTime()),'6','8',36000)
        #print process_string
