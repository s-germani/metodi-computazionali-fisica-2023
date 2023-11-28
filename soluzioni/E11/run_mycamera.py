#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Utilizzo del Modulo  mycamera                   #
#    che sfrutta la libreria condivisa mycamera     #
#####################################################


import numpy as np
import matplotlib.pyplot  as plt

import mycamera




width  = 1536
height = 1024
photo = np.zeros((height,width))


buffer_size = width * height * 2

data = mycamera.read_camera(buffer_size)




for i in range(0,len(data),2):
    x = (i // 2)  % width
    y = (i // 2) // width 
    pixel_value = int.from_bytes(data[i]+data[i+1], byteorder='little', signed=False)
    photo[y,x] = pixel_value
    


plt.subplots(figsize=(16,9))
plt.imshow(photo, origin='lower', norm='log', cmap='gray')
plt.colorbar()
plt.axis('off')
plt.show()

