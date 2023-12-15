#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 10 - Metodi Monte Carlo             #
#                                                   #
#   script  per plot  Diffusione 2D                 #
#                                                   #
#####################################################


import sys,os
import numpy as np
import pandas as pd

from scipy import integrate

import matplotlib.pyplot as plt

import argparse

import random_walk as rw
               
#####################################################################
#      Funzione per gestione opzioni (argparse)                     #
#####################################################################

def parse_arguments():

    parser = argparse.ArgumentParser(description='Plot su random walk 2D.',
                                     usage      ='python3 diffusione_2d.py  --option')
    parser.add_argument('--symm',   action='store_true',    help='Plot diffusione 2D simmetrica')
    parser.add_argument('--asymm',  action='store_true',    help='Plot diffusione 2D asimmetrica')
    parser.add_argument('--efield', action='store_true',    help='Plot diffusione 2D con campo elettrico')
    parser.add_argument('--dist',   action='store_true',    help='Plot distanze')
    
    return  parser.parse_args()





#####################################################################
#            Funzione principale per grafici                        #
#####################################################################

               
def diffusione_2d():
    """
    Funzione che utilizza il modulo random_walk mostra grafici per la diffusione 2D simmetrica e asimmetrica
    """

    
    args = parse_arguments()

    # Definizione lunghezza passo (step) e numero passi
    step    = 1
    Nsteps5 = 10000
    Nsteps  = 1000
    MaxDist = 200

    #--------------------------------------------------------#
    #  Random Walk  Unforme                                  # 
    #--------------------------------------------------------#
    if args.symm == True:


        ### --------------- plot  5 walker ----------------------

        # Liste per gli array con le posizioni dei random walker
        xx5 = []
        yy5 = []
        
        # Ciclo per calcolo 5 random walk uniformi da 1000 passi 
        plt.subplots(figsize=(9,8))
        for i in range(5):
            x0,y0 = rw.random_walk2d(step, Nsteps5)
            xx5.append(x0)
            yy5.append(y0)
            plt.scatter(x0,y0, s=3)

        plt.xlabel(r'$\Delta x$')
        plt.ylabel(r'$\Delta y$')
        plt.xlim(-200, 200)
        plt.ylim(-200, 200)
        plt.show()


        
        ### --------------- plot  1000 walker --------------------

        # Calcolo per 100 walker a diversi passi (10, 100, 1000)
        Nwalkers = 100

        # Array per posizioni walker
        x10   = np.empty(0)
        y10   = np.empty(0)
        x100  = np.empty(0)
        y100  = np.empty(0)
        x1000 = np.empty(0)
        y1000 = np.empty(0)


        # Ciclo per i 1000 walker
        for iw in range(Nwalkers):

            # Posizioni x,y per walker iw 
            xw,yw = rw.random_walk2d(step, Nsteps)

            # Posizione al passo 1000
            x1000 = np.append(x1000, xw[-1])
            y1000 = np.append(y1000, yw[-1])

            # Posizione al passo 100
            x100  = np.append(x100, xw[99])
            y100  = np.append(y100, yw[99])

            # Posizione al passo 10
            x10   = np.append(x10, xw[9])
            y10   = np.append(y10, yw[9])

            # Somma delle distanze e delle distanze al quadrato
            #dsqm = dsqm + (xw**2+yw**2)
            #dm   = dm  + np.sqrt(xw**2+yw**2)


        # distanza media e quadratica media
        #dsqm = dsqm/Nwalkers
        #dm   = dm/Nwalkers


        #Grafico posizione walker dopo 10, 100, 1000 passi 
        plt.scatter(x1000,y1000, s=10, alpha=0.8, label='{:d} steps'.format(    Nsteps   ))
        plt.scatter(x100, y100,  s=10, alpha=0.7, label='{:d} steps'.format(int(Nsteps/10)))
        plt.scatter(x10,  y10,   s=10, alpha=0.6, label='{:d} steps'.format(int(Nsteps/100)))
        plt.xlabel(r'$\Delta x$', fontsize=14)
        plt.ylabel(r'$\Delta y$', fontsize=14)
        plt.xlim(-75, 75)
        plt.ylim(-75, 75)
        plt.legend(fontsize=12)
        plt.show()


        
        ### --------------- plot  5 walker con due pannelli ---------------
        
        fig, ax = plt.subplots(1,2, figsize=(14,8))
        for i in range(5):
            ax[0].scatter(xx5[i],yy5[i], s=3)
            ax[1].plot(np.sqrt(xx5[i]**2+yy5[i]**2) )

        ax[0].set_xlabel(r'$\Delta x$')
        ax[0].set_ylabel(r'$\Delta y$')
        ax[0].set_xlim(-200, 200)
        ax[0].set_ylim(-200, 200)

        ax[1].set_xlabel('step')
        ax[1].set_ylabel(r'$d^2$')
        ax[1].set_ylim(0, 250)

        plt.show()




        
    #--------------------------------------------------------#
    #  Random Walk Non Unforme                               # 
    #--------------------------------------------------------#

    if args.asymm == True:
        
        # Ciclo per calcolo 5 random walk non uniformi da 1000 passi     
        fig,ax = plt.subplots(1,2, figsize=(16,8))
        for i in range(5):
            x0pphi,y0pphi = rw.random_walk2d_pphi(step, Nsteps5)

            ax[0].scatter(x0pphi,y0pphi, s=3)
            ax[1].scatter(x0pphi,y0pphi, s=3)

        ax[0].set_xlabel(r'$\Delta x$')
        ax[0].set_ylabel(r'$\Delta y$')
        ax[1].set_xlabel(r'$\Delta x$')
        ax[1].set_ylabel(r'$\Delta y$')
        ax[0].set_xlim(-4000, 4000)
        ax[0].set_ylim(-4000, 4000)
        ax[1].set_xlim(-4000, 200)
        ax[1].set_ylim(-200,  200)

        plt.show()





    #--------------------------------------------------------#
    #  Random Walk con emulazione Campo Elettrico Costante   # 
    #--------------------------------------------------------#

    if args.efield == True:
        
        # Ciclo per calcolo 5 random walk non uniformi da 1000 passi     
        fig,ax = plt.subplots(1,2, figsize=(16,8))
        for i in range(5):
            x0pphi,y0pphi = rw.random_walk2d_E(step, MaxDist, 0.01*step)

            ax[0].scatter(x0pphi,y0pphi, s=3)
            ax[1].scatter(x0pphi,y0pphi, s=3)

        ax[0].set_xlabel(r'$\Delta x$')
        ax[0].set_ylabel(r'$\Delta y$')
        ax[1].set_xlabel(r'$\Delta x$')
        ax[1].set_ylabel(r'$\Delta y$')
        ax[0].set_xlim(-1.1*MaxDist*1.1, 1.1*MaxDist)
        ax[0].set_ylim(-1.1*MaxDist*1.1, 1.1*MaxDist)
        ax[1].set_xlim(-20,  MaxDist*1.1)
        ax[1].set_ylim(-100, 100)

        plt.show()



    #--------------------------------------------------------#
    #  Disatnza Random Walk Unforme                          # 
    #--------------------------------------------------------#

    if args.dist == True:
        
        # Calcolo per 1000 walker
        Nwalkers = 500


        # Array per calcolo media e media quadratica
        dsqm  = np.zeros(Nsteps+1)
        dm    = np.zeros(Nsteps+1)

        # Ciclo per i 1000 walker
        for iw in range(Nwalkers):

            # Posizioni x,y per walker iw 
            xw,yw = rw.random_walk2d(step, Nsteps)

            # Somma delle distanze e delle distanze al quadrato
            dsqm = dsqm + (xw**2+yw**2)
            dm   = dm  + np.sqrt(xw**2+yw**2)


        # distanza media e quadratica media
        dsqm = dsqm/Nwalkers
        dm   = dm/Nwalkers


        # Grafico distanza e distanza quadratica media in funzione del numero di passi
        fig, ax = plt.subplots(1,2, figsize=(14,8))

        ax[0].plot(dm)
        ax[0].set_xlabel(r'Passi', fontsize=14)
        ax[0].set_ylabel(r'$\left< d \right>$', fontsize=14)

        ax[1].plot(dsqm)
        ax[1].set_xlabel(r'Passi', fontsize=14)
        ax[1].set_ylabel(r'$\left< d^2 \right>$', fontsize=14)

        plt.show()


                         
if __name__ == "__main__":

    diffusione_2d()
