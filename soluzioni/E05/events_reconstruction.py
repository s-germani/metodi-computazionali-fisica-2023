#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 5 - Funzioni Moduli e Classi:       #
#                                                   #
#   Ricostruzione degli eventi nei file di dati     #
#     a utilizzando il modulo reco                  #
#                                                   #
#####################################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import reco



fM0 = 'hit_times_M0.csv'
fM1 = 'hit_times_M1.csv'
fM2 = 'hit_times_M2.csv'
fM3 = 'hit_times_M3.csv'



def get_hits(hf):
    """
    Funzione che legge un file csv e restituisce un array di reco.Hits

    get_hits(hf)

    Parametri
    -------------------

    hf : nome o percorso file di dati

    Restituisce:
    ------------------

    hits: array di oggetti di tipo Hit

    """
    
    df = pd.read_csv(hf)

    hits = np.array([reco.Hit( r['mod_id'], r['det_id'], r['hit_time'] ) for i, r in df.iterrows() ])
    
    return hits



        
def reconstruct():
    """
    Funzione principale che produce i grafici richiesti
    """

    # Lettura file e creazione array di Hit 
    hitsM0 = get_hits( fM0 )
    hitsM1 = get_hits( fM2 )
    hitsM2 = get_hits( fM1 )
    hitsM3 = get_hits( fM3 )

    hits = np.concatenate( (hitsM0, hitsM1, hitsM2, hitsM3) )


    # Ordino array concatenato
    hits.sort(kind='mergesort' )


    print('Total Number of Hitss:', hits.size)
    


    # Differenza temporale fra hit successivi
    hit_dt  = np.diff(hits).astype(float)


    # Maskera per selezionare Delta t > 0
    dtmask = hit_dt > 0

    # Grafico log10 tempi Hit - asse y in scala lienare
    plt.hist(np.log10(hit_dt[dtmask]), bins=100)
    plt.xlabel(r'$log_{10}(\Delta t)$ [ns]')
    plt.show()


    # Grafico log10 tempi Hit - asse y in  scala logaritmica
    plt.hist(np.log10(hit_dt[dtmask]), bins=100)
    plt.xlabel(r'$log_{10}(\Delta t)$ [ns]')
    plt.yscale('log')
    plt.show()


    # Grafico tempi Hit con bin logaritmicamente spaziati e assi in scala logaritmica)
    logbins = np.logspace(0, 6, 100)
    plt.hist(hit_dt[dtmask], bins=logbins)
    plt.xlabel(r'$\Delta t$ [ns]')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    
    
if __name__ == "__main__":

    reconstruct()
