import multiprocessing

if __name__ == '__main__':
    print "Elija una de las siguientes opciones:\n"
    option = 1
    while option!=0:
        option = int(raw_input(" 1) Hacer llamada\n 2) Enviar mensaje\n 3) Revisar contactos\n 4) Revisar historial de llamadas\n 5) Ver mensajes\n 6) Ejecutar proceso\n 7) Ver Procesos\n 0) Salir\n"))
        if option == 1:
            # hacer llamada. Pedir el numero y dar la opcion de cortar
            pass
        elif option == 2:
            #pedir numero y texto para enviar un mensaje por consola, ojo con las interrupciones
            pass
        elif option == 3:
            # Revisar contactos. Se debe poder realizar una llamada a partir de los contactos (nombre de la persona)
            pass
        elif option == 4:
            pass
        elif option == 5:
            pass
        elif option == 6:
            pass
        elif option == 7:
            pass
        elif option == 0:
            break