import multiprocessing
import Scheduler
import tkFileDialog
import multiprocessing
import time
import thread
import threading
import GUI

def _gui_init(so):
    GUI.GUI(so)

if __name__ == '__main__':
   
    so = Scheduler.Scheduler()
    thread.start_new_thread(_gui_init,(so,)) # iniciamos la GUI en un thread aparte
    
    #prueba
    so.loadProcesses() # Cargamos examples.txt
    so.priorityScheduler() # Comenzamos el Loop