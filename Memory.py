# -*- coding: utf-8 -*-

import os
import pickle

class Memory:
    
    @staticmethod
    def fileName(pid):
        return 'Memory/p%i.txt' % pid # devuelve el nombre del archivo donde esta guardado el proceso
    
    @staticmethod
    def saveProcess(process):
        f = open(Memory.fileName(process.pid),'wb') # w abre para escribir y si archivo existe lo borra, b hace que en windows se pase en binary data
        pickle.dump(process, f) # esto guarda el objeto serializado
        f.close()
        
    @staticmethod
    def loadProcess(pid):
        #print "Loading from memory pid = %i" % pid
        filePath = Memory.fileName(pid)
        if os.path.exists(filePath):
            f = open(filePath,'rb') # r abre para leer, y b me dice que lo haga en binario
            p = pickle.load(f) # esto corresponde a una instancia de nuestra clase "Process"
            return p
        return None # si no est� en memoria el proceso
    
    @staticmethod
    def readProcess(pid):
        filePath = Memory.fileName(pid)
        if os.path.exists(filePath):
            f = open(filePath,'rb') # r abre para leer, y b me dice que lo haga en binario
            p = pickle.load(f) # esto corresponde a una instancia de nuestra clase "Process"
            return p
        return None # si no est� en memoria el proceso

    @staticmethod
    def removeProcess(pid):
        #print "Removing from memory pid = %i " % pid
        try:
            os.remove(Memory.fileName(pid))
            return True
        except:
            return False
        
        