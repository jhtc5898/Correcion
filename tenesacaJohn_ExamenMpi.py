from mpi4py import MPI

import random
import time

resultPar = 0

def how_many_max_values_sequential(ar):
    maxValue = 0
    for i in range(len(ar)):
        if i == 0:
            maxValue = ar[i]
        else:
            if ar[i] > maxValue:
                maxValue = ar[i]
    contValue = 0
    for i in range(len(ar)):
        if ar[i] == maxValue:
            contValue += 1

    return contValue
def how_many_max_values_parallel(ar):
    
    comm = MPI.COMM_WORLD #Comunicador
    numtasks = comm.size
    rank = comm.Get_rank()#Numero De Procesos
    #print(rank)

    numworkers = numtasks -1 #Recorrido
    
    if(rank == 0):
        averow = len(ar)//numworkers#Recorrido
       
        comp = len(ar)%numworkers#Comparador 0 inicio 
        
        offset = 0
        mtype = 1
        
        for dest in range(numworkers):
            if(dest+1 <= comp):
                rows = averow+1
            else:
                rows = averow
            #Envio
            #print("task "+str(dest+1));
            comm.send(offset,dest=dest+1,tag=mtype)
            comm.send(rows,dest=dest+1,tag=mtype)
            comm.send(ar[offset:rows+offset],dest=dest+1,tag=mtype)
            offset = offset + rows
            
        resultPar = 0
        mtype = 2
        for i in range(numworkers):
            source = i
            offset = comm.recv(source=source+1,tag=mtype)
            rows = comm.recv(source=source+1,tag=mtype)
            tot = comm.recv(source=source+1,tag=mtype)
            resultPar = resultPar+tot
        return resultPar
            
    if(rank > 0):
        mtype = 1
        offset = comm.recv(source=0,tag=mtype)
        rows = comm.recv(source=0,tag=mtype)
        
        ar = comm.recv(source=0,tag=mtype)#Matriz 
        
        maxValue = 0
        for i in range(len(ar)):
            if i == 0:
                maxValue = ar[i]
            else:
                if ar[i] > maxValue:
                    maxValue = ar[i]
        contValue = 0
        for i in range(len(ar)):
            if ar[i] == maxValue:
                contValue += 1
                
        mtype = 2
        #Envio
        comm.send(offset,dest=0,tag=mtype)
        comm.send(rows,dest=0,tag=mtype)
        comm.send(contValue,dest=0,tag=mtype)
    
if __name__ == '__main__':
    


    ar_count = 40000000

    #Generate ar_count random numbers between 1 and 30
    ar = [random.randrange(1,30) for i in range(ar_count)]
    

    inicioSec = time.time()
    resultSec = how_many_max_values_sequential(ar)
    finSec =  time.time()

    
    

    inicioPar = time.time()  
    resultPar = how_many_max_values_parallel(ar)
    finPar = time.time()
    

   
    print(resultSec)

    
    
    print('Results are correct!\n' if resultSec == resultPar else 'Results are incorrect!\n')

    print('Sequential Process took %.3f ms with %d items\n' % ((finSec - inicioSec)*1000, ar_count))

    print('Parallel Process took %.3f ms with %d items\n' % ((finPar - inicioPar)*1000, ar_count))