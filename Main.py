import Scheduler
import thread
import GUI

def _gui_init(so):
    GUI.GUI(so)

if __name__ == '__main__':
   
    so = Scheduler.Scheduler()
    thread.start_new_thread(_gui_init,(so,)) # iniciamos la GUI en un thread aparte
    
    so.loadProcesses() # Cargamos examples.txt
    #Tarea1
    #so.priorityScheduler() # Comenzamos el Loop
    
    #Tarea2
    tarea2='esta_variable_hace_que_se_ejecute_la_tarea_2'
    so.priorityScheduler(tarea2)
    