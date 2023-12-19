#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Definizione del modulo  serie                   #
#    che utilizza solo codice python                #
#    per il calcolo della successione di Fibonacci  #
#####################################################


def fibonacci(n):
  
  if n>2:
    vm1 = 1
    vm2 = 0

    vv = 0
      
    
    for i in range(n+1):
      vv = vm2+vm1
      vm2 = vm1
      vm1 = vv
    
    return vm1/vm2;

  else:
    return 1


