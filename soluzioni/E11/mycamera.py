#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Definizione del modulo  mycamera                #
#    che sfrutta la libreria condivisa mycamera     #
#####################################################

import numpy
import ctypes

_libmycamera = numpy.ctypeslib.load_library('libmycamera', '.')


_libmycamera.read_camera.argtypes = [ctypes.c_char_p]
_libmycamera.read_camera.restype  = ctypes.c_int



def read_camera(size):
    """
    read_camera(size)
    
    acquisisce l'immagine della fotocamera attraverso la libreria mycamera
    i dati per l'immagine acquisita corrispondono a 2 bytes / pixel

    Parametri
    ---------------
    size : dimensione dell'immagine in bytes (height * width * 2)

    Restituisce
    ---------------
    p_image : array di bytes di dimensione (height * width * 2)    
    """

    p_image = ctypes.create_string_buffer(size)
    err = _libmycamera.read_camera(p_image)
    print('Image Size: {:}  bytes'.format( len(p_image) ) )
    return p_image




    


