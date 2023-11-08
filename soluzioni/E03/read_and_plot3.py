#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 3 - Numpy, Pandas, Matplotlib:      #
#                                                   #
#   Lettura File CSV (nella sottocartella dati)     #
#   + prduzione scatter plot e istogrammi           #
#     in immagine con più riquqdri                  #
#                                                   #
#####################################################

import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

################################### Dati Input  ##########################################
# Lettura file 
#catdf = pd.read_csv('dati/4LAC_DR2_sel.csv')
catdf = pd.read_csv('4LAC_DR2_sel.csv')

print('Columns:', catdf.columns)
print(catdf)





#############################  Scatter plot     ##########################################

# Creo riquadro figura
fig = plt.figure(figsize=(12,11))

# creo griglia 2x2 per subplot con asse X in comune per le colonne e asse Y inb comune per le righe 
gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
ax = gs.subplots( sharex='col', sharey='row')

## Scatter plot PL Index vs. log(nu_syn) for different source classes
ax[1,0].scatter(np.log10(catdf.loc[ catdf['CLASS']=='bll',  'nu_syn']), catdf.loc[ catdf['CLASS']=='bll', 'PL_Index'] , color='limegreen',  alpha=0.3, label='bll')
ax[1,0].scatter(np.log10(catdf.loc[ catdf['CLASS']=='fsrq', 'nu_syn']), catdf.loc[ catdf['CLASS']=='fsrq','PL_Index'] , color='darkorange', alpha=0.3, label='fsrq')
ax[1,0].tick_params(axis='both', which='major', labelsize=14)
ax[1,0].set_xlabel(r'log($\nu_{syn}$ [Hz])',    fontsize=16)
ax[1,0].set_ylabel('PL Index',                  fontsize=16)
ax[1,0].legend(fontsize=16)



# Istogramma nu_syn
ax[0,0].hist(np.log10(catdf.loc[ catdf['CLASS']=='bll',  'nu_syn']), bins=50, range=(10,20), color='limegreen',  alpha=1.0, label='bll')
ax[0,0].hist(np.log10(catdf.loc[ catdf['CLASS']=='fsrq', 'nu_syn']), bins=50, range=(10,20), color='darkorange', alpha=0.4, label='fsrq')
ax[0,0].tick_params(axis='both', which='major', labelsize=14)
ax[0,0].set_ylabel(r'Number of sources',        fontsize=16)
ax[0,0].legend(fontsize=16)


# Istogramma PL_Index con barre orizzontali
ax[1,1].hist(catdf.loc[ catdf['CLASS']=='bll', 'PL_Index'], bins=50, range=(1,3.5), color='limegreen',  alpha=1.0, orientation='horizontal', label='bll')
ax[1,1].hist(catdf.loc[ catdf['CLASS']=='fsrq','PL_Index'], bins=50, range=(1,3.5), color='darkorange', alpha=0.4, orientation='horizontal', label='fsrq')
ax[1,1].tick_params(axis='both', which='major', labelsize=14)
ax[1,1].set_xlabel( 'Number of sources',        fontsize=16)
ax[1,1].legend(fontsize=16)


# Rimuovo assi per riqyadro non necessario
ax[0,1].axis('off')


plt.savefig('Blazars_4LAC_PLindex_vs_SynPeak.pdf')
plt.savefig('Blazars_4LAC_PLindex_vs_SynPeak.png')
plt.show()






