#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Script che esegue i moduly sviluppati           #
#    per il calcolo della successione di Fibonacci  #
#    - serie   : basato sulla libreria libserie.so  #
#    - serie_py: basato  su puro codice python      #
#####################################################

import numpy as np
import serie_py
import serie

import time


#### uso serie da libreria C libserie.so ####
start_time1 = time.time()

print(serie.fibonacci(1000))

stop_time1 = time.time()


print('>>>>', stop_time1 - start_time1)


#### uso serie da modulo python serie_py  #####
start_time2 = time.time()
print(serie_py.fibonacci(1000))

stop_time2 = time.time()

print('>>>>', stop_time2 - start_time2)



