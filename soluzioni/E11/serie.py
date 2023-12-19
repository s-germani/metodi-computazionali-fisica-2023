#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Definizione del modulo  serie                   #
#    che sfrutta la libreria condivisa serie        #
#    per il calcolo della successione di Fibonacci  #
#####################################################


import numpy
import ctypes

_libserie = numpy.ctypeslib.load_library('libserie', '.')


_libserie.fibonacci.argtypes = [ctypes.c_int]
_libserie.fibonacci.restype  = ctypes.c_double



def fibonacci(n):
    return _libserie.fibonacci(int(n))


