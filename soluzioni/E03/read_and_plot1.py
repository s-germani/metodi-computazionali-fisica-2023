#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 3 - Numpy, Pandas, Matplotlib:      #
#                                                   #
#   Lettura File CSV (nella sottocartella dati)     #
#   + prduzione grafici curva dil luce              #
#                                                   #
#####################################################

import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

################################### Dati Input  ##########################################
# Lettura file 
lcdf = pd.read_csv('dati/4FGL_J2202.7+4216_weekly_9_11_2023.csv')

print('Columns:', lcdf.columns)
#print(lcdf)


#############################  Grafici senza errori  #####################################

## grafico Flusso vs. Data
plt.subplots(figsize=(12,6))
plt.plot(lcdf['Julian Date'], lcdf['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'] )
plt.xlabel('Julian Date', fontsize=14)
plt.ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()


## grafico Flusso vs. Data con simbolo (no linea)
plt.subplots(figsize=(12,6))
plt.plot(lcdf['Julian Date'], lcdf['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'], 'o', color='royalblue' )
plt.xlabel('Julian Date', fontsize=14)
plt.ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()



#############################  Grafici con  errori  #####################################

## grafico Flusso vs. Data salvato come png e pdf
plt.subplots(figsize=(12,6))
plt.errorbar(lcdf['Julian Date'], lcdf['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],  yerr=lcdf['Photon Flux Error(photons cm-2 s-1)'], fmt='o', color='limegreen' )
plt.xlabel('Julian Date', fontsize=14)
plt.ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig('curva_luce.png')
plt.savefig('curva_luce.pdf')
plt.show()
    
        
## grafico Flusso vs. Data  logy  salvato come png e pdf
plt.subplots(figsize=(12,6))
plt.errorbar(lcdf['Julian Date'], lcdf['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],  yerr=lcdf['Photon Flux Error(photons cm-2 s-1)'], fmt='.', color='limegreen' )
plt.xlabel('Julian Date', fontsize=14)
plt.ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.yscale('log')
plt.savefig('curva_luce_logy.png')
plt.savefig('curva_luce_logy.pdf')
plt.show()





