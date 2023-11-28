#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Definizione Classe myCamera                     #
#    che sfrutta la libreria condivisa mycamera     #
#####################################################


import numpy as np
import ctypes

import matplotlib.pyplot  as plt


class myCamera:

    """
    Classe che fornisce l'interfaccia per l'accesso alla camera myCamera tramite la libreria condivisa mycamera
    
    """
        
    _libmycamera = np.ctypeslib.load_library('libmycamera', '.')

    _height = 1024
    _width  = 1536

    # Pointer to raw image 
    _p_image = None

    # Decoded Image 
    _image   = None

    _colorbar = True

    _image_file = ''
    
    def __init__(self):
        # Init ctypes param types and return values
        self._libmycamera.read_camera.argtypes = [ctypes.c_char_p]
        self._libmycamera.read_camera.restype  = ctypes.c_int

        self.compute_image_bytes()

        
    def compute_image_bytes(self):
        """
        calcolo bytes necessari per immagazzianre l'immagine acquisita 
          immagine = _height * _width pixels  
          2 bytes / pixel 
          bytes = _height * _width * 2 
        """
        self._image_bytes = self._height * self._width * 2 
        

    def read_camera(self):
        """
        Acquisizione immagine
        """
        self._p_image = ctypes.create_string_buffer(self._image_bytes)
        err = self._libmycamera.read_camera(self._p_image)
        print('Image Size: {:}  bytes'.format( len(self._p_image) ) )

        self.decode_rawimage()

        
    def get_rawimage(self):
        """
        Restituisce immagine in formato binario (array di bytes di dimensione: height * width * 2  )
        """

        return self._p_image

    
    def decode_rawimage(self):
        """
        Decodifica  immagine aquisita
           (chiamata automaticamente dopo l'acquisizione dell'immagine) 
        """

        self._image = np.zeros((self._height, self._width))
        
        for i in range(0,len(self._p_image),2):
            
            x = (i // 2)  % self._width
            y = (i // 2) // self._width 

            pixel_value = int.from_bytes(self._p_image[i]+self._p_image[i+1], byteorder='little', signed=False)
            
            self._image[y,x] = pixel_value

            
    def get_image(self):
        """
        Restituisce immagine decodificata (array di int di dimensione: height * width)
        """
        
        return self._image


    def set_image_file(self, image_file):
        """
        Imposta file in cui salvare l'immagine
           se il nome file non è impostato (default) l'immagine non viene salvata
        """

        self._image_file = image_file

        
    def set_colorbar(self, cb):
        """
        Imposta visualizzazione colorbar
        """

        self._colorbar = cb

    def show_image(self, nrm='log', cm='gray'):
        """
        Visulaizza immagine
        """

        
        plt.subplots(figsize=(16,9))
        plt.imshow(self._image, origin='lower', norm=nrm, cmap=cm)
        if self._colorbar == True:
            plt.colorbar()
        plt.axis('off')
        if self._image_file != '':
            plt.savefig(self._image_file)
        plt.show()

        

    def save_image(self, nrm='log', cm='gray'):
        """
        Salva immagine senza visualizzarla
        """

        if self._image_file != '':
            plt.subplots(figsize=(16,9))
            plt.imshow(self._image, origin='lower', norm=nrm, cmap=cm)
            if self._colorbar == True:
                plt.colorbar()
            plt.axis('off')
    
            plt.savefig(self._image_file)
            plt.close()


    def __str__(self):
        prntstr =  '------------------------------------------------------------\n'
        prntstr += 'Dimensione Immagine: {:d} x {:d} pixels = {:d} bytes\n'.format(self._width, self._height, self._image_bytes)
        if self._image_file != '':
            prntstr += 'File Immagine: {:}\n'.format(self._image_file)  
        prntstr +=  '------------------------------------------------------------'
        return prntstr
    
