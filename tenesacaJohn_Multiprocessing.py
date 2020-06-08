import random

import time
import multiprocessing


 

 

def how_many_max_values_sequential(ar):
    #find max value of the list

    maxValue = 0

    for i in range(len(ar)):

        if i == 0:

            maxValue = ar[i]

        else:

            if ar[i] > maxValue:

                maxValue = ar[i]
               
    #find how many max values are in the list

    contValue = 0

    for i in range(len(ar)):

        if ar[i] == maxValue:

            contValue += 1
    return contValue

 

# Complete the how_many_max_values_parallel function below.

def how_many_max_values_parallelProceso(ar):

   numDatos=[ar[0:5000000],ar[5000000:10000000],ar[10000000:15000000],ar[15000000:20000000],ar[20000000:25000000],ar[25000000:30000000],ar[30000000:35000000],ar[35000000:40000000]]
   tot=0
   numProcesos=8
   pool = multiprocessing.Pool(numProcesos)
   resultado=pool.map(multip,numDatos)
   pool.close()
   pool.join()

   for i in resultado:
       tot=tot+i
   
   return tot

def multip(ar):
    #find max value of the list

    maxValue = 0

    for i in range(len(ar)):

        if i == 0:

            maxValue = ar[i]

        else:

            if ar[i] > maxValue:

                maxValue = ar[i]
               
    #find how many max values are in the list

    contValue = 0

    for i in range(len(ar)):

        if ar[i] == maxValue:

            contValue += 1
    return contValue


if __name__ == '__main__':
    
    ar_count = 40000000

    #Generate ar_count random numbers between 1 and 30

    ar = [random.randrange(1,30) for i in range(ar_count)]
    
    

    inicioSec = time.time()

    resultSec = how_many_max_values_sequential(ar)

    finSec =  time.time()

   

    inicioPar = time.time()   

    resultPar = how_many_max_values_parallelProceso(ar)
    

    finPar = time.time() 

   

    print('Results are correct!\n' if resultSec == resultPar else 'Results are incorrect!\n')

    print('Sequential Process took %.3f ms with %d items\n' % ((finSec - inicioSec)*1000, ar_count))

    print('Parallel Process took %.3f ms with %d items\n' % ((finPar - inicioPar)*1000, ar_count))

