#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 10 - Metodi Monte Carlo:            #
#                                                   #
#   Classe myMWPC  per simulare  la deriva degli    #
#     elettroni primari generato da una traccia in  #
#     una Camera Proporzionale a Molti Fili         #
#                                                   #
#####################################################

import numpy as np

class myMWPC:
    """
    Classe myMWPC(mnp=5, gap=1, su=1e-5, sf=1e-7, nr=2e7, tc=1e-12)

      Input 
        mnp : numero medio di coppie elettrone ione
        gap : spessore gap MWPC (cm)
        su  : step size diffusione (cm)
        sf  : step size costante dal campo elettrico(cm)
        nr  : numero medio di steps prima della recombinazione
        tc  : tempo medio fra due collisioni 
    """

    _ndet = 0           # detected electrons
    _dt   = np.empty(0) # drift times
    
    def __init__(self, mnp=5, gap=1, su=1e-5, sf=1e-7, nr=2e7, tc=1e-12):

        self._mnp = mnp # numero medio di coppie elettrone ione
        self._gap = gap # spessore gap MWPC (cm)
        self._su  = su  # uniform step size (cm)
        self._sf  = sf  # field related step size (cm)
        self._nr  = nr  # mean number of steps before recombination
        self._tc  = tc  # mean time between collisions

        
    def simulate_track(self):
        """
        Simulazione di una traccia 
          numero di coppie primarie fluttuato poissonianamente con media _np
          posizione delle coppie primarie (.pos)  distribuita uniformemente
        """

        self._np  = np.random.poisson(self._mnp)
        self._pos = np.random.uniform(-self._gap/2, self._gap/2, self._np) 

        self.drift_all_pairs()

        return self._np, self._nr, self._pos, self._dt


        
    def get_primary_npairs(self):
        """
        Restituice il numero di coppie primarie
        """
        return self._np 

 

    def drift_all_pairs(self):
        """
        Esegue ciclo su elettroni  primari per simulare la diffusione
        """

        self._dt = np.empty(0)
        
        for p in self._pos:
            dt = self.drift(p)
            if dt > 0:
                self._ndet += 1
                self._dt = np.append(self._dt, dt)


    def recombine(self):
        """
        Calcola se l'elettrone viene ricombinato p=1/_nr
        """
        if np.random.uniform() > 1/self._nr:
            return False
        else:
            return True


        
    def drift(self, spos):
        """
        Simula la deriva di un elttrone a partore dalla posizione spos

        Restituisce:
          il numero di step per la rivelazione (-1 se l'elettrone non viene rivelato)
        """
        
        recombined = False
        detected   = False

        pos    = spos
        nsteps = 0

        while not(recombined) and not(detected):

            recombined = self.recombine()

            df =  -np.sign(pos)*self._sf
            dpp = -np.sin(np.random.uniform(low=0, high=2*np.pi) )
            dp =  self._su * dpp  + df 

            pos += dp
            nsteps += 1

            if abs(pos) < 0.01:
                detected = True

        if detected:
             return nsteps*self._tc
        else:
             return -1
        
            
        
        
     
