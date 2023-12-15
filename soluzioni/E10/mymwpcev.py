#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 10 - Metodi Monte Carlo:            #
#                                                   #
#   Classe myMWPCev per descrivere gli eventi di    #
#     Camera Proporzionale a Molti Fili             #
#                                                   #
#####################################################

import numpy as np


class myMWPCev:

    """
    Classe myMWPCev(npp, nrp, pos, dt) 
    
      Input:
        np  : numero di coppie primarie
        nr  : numero di coppie rivelate
        pos :  # posizioni coppie primarie
        dt  : tempi di deriva

      Attributi:
        _np
        _nr 
        _pos
        _dt 

    """

    def __init__(self, npp, nrp, pos, dt):

        self._np  = npp  # numero di coppie primarie
        self._nr  = nrp  # numero di coppie rivelate
        self._pos = pos  # posizioni coppie primarie
        self._dt  = dt   # tempi di deriva


        if self._nr > 0:
            self._dt_first = np.sort(self._dt)[0]
            self._dt_mean  = np.mean(self._dt)
        else:
            self._dt_first = 0
            self._dt_mean  = 0

        
        
    def get_dt_first(self):
        """
        Restituisce il tempo di deriva minore tra gli elettroni rivelati
        """
        return self._dt_first

    def get_dt_mean(self):
        """
        Restituisce il tempo di deriva medio degli elettroni rivelati
        """
        return self._dt_mean

    
