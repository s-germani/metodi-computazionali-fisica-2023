#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 5 - Moduli e Classi:                #
#                                                   #
#   Modulo reco con classi Hit ed Event             #
#      per la ricostruzione di eventi nei dati      #
#                                                   #
#####################################################


import numpy as np


class Hit:

    """
    Classe che definisce gli hit di un rivelatore suddividi in Moduli ognuno dei quali contiene diversi sensori
    
    Attributi:
    mid  : Id Modulo
    sid  : Id Sensore
    time : Time Stamp rivelazione
    """

    def __init__(self, mid, sid, time):

        self.mid     = mid  # module id
        self.sid     = sid  # single detector id inside module
        self.time    = time
        #self.signal  = signal


    def __eq__(self, other) :
        return self.time == other.time

    def __lt__(self, other) :
        if self.time == other.time:
            return 10*self.mid+self.sid < 10*other.mid+other.sid
        else:
            return self.time < other.time

    def __gt__(self, other) :
        return self.time > other.time

    def __sub__(self, other) :
        return self.time - other.time

    
