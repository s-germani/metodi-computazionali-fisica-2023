#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 6 - Integrazione e Derivazione:     #
#                                                   #
#   Distanza percorsa da velocità                   #
#                                                   #
#####################################################



import sys,os
import numpy as np
import pandas as pd

from scipy import integrate

import matplotlib.pyplot as plt

import argparse

##---------------------------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calcolo distanza percorsa da velocità.')
    parser.add_argument('-f', '--file',    action='store',      default='vel_vs_time.csv', help='File di input')
    parser.add_argument('-v', '--vel',     action='store_true',                            help='Grafico Velocità vs Tempo')
    parser.add_argument('-d', '--dist',    action='store_true',                            help='Grafico Distanza vs Tempo')
    return  parser.parse_args()



##---------------------------------------------

def distanza():


    args = parse_arguments()
    
    # Lettura file 
    veldf = pd.read_csv(args.file)

    # Colonne Data Frame
    print('Colonne File:', veldf.columns)


    if args.vel == True:

        ## grafico velocità vs tempo
        plt.plot(veldf['t'], veldf['v'])
        plt.xlabel('tempo [s]')
        plt.ylabel('velocità [m/s]')
        plt.show()


    if args.dist == True:

        # Array per le distanze
        dists = np.array([])


        # Ciclo su intervalli temporali 
        for iv in range(1, len(veldf['v'])+1): 
            # integrale per distanza nell'intevallo temporale 0-iv
            idists = integrate.simpson(veldf['v'][:iv],   dx=0.5)
            # appendo valore dell'integrale all'array di distanze
            dists = np.append(dists, idists)


        ## grafico distanza vs tempo
        plt.plot(veldf['t'], dists)
        plt.xlabel('tempo [s]')
        plt.ylabel('distanza percorsa [m]')
        plt.show()




###########################################################################

if __name__ == "__main__":

    distanza()

