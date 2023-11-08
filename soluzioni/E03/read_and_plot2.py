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
#                                                   #
#####################################################

import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

################################### Dati Input  ##########################################
# Lettura file 
catdf = pd.read_csv('dati/4LAC_DR2_sel.csv')

print('Columns:', catdf.columns)
print(catdf)


#############################  Scatter plot     ##########################################

## Scatter plot Indice Spettrale vs. Flusso
plt.subplots(figsize=(10,6))
plt.scatter(catdf['Flux1000'], catdf['PL_Index'] )
plt.xlabel('Flux (photons cm-2 s-1)', fontsize=14)
plt.ylabel('PL Index', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()



## Scatter plot Indice Spettrale vs. Flusso  logx
plt.subplots(figsize=(10,6))
plt.scatter(catdf['Flux1000'], catdf['PL_Index'] )
plt.xlabel('Flux (photons cm-2 s-1)', fontsize=14)
plt.ylabel('PL Index', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xscale('log')
plt.show()




## Scatter plot PL Index vs. log(nu_syn)
plt.subplots(figsize=(10,6))
plt.scatter(np.log10(catdf['nu_syn']), catdf['PL_Index'] , color='darkred' )
plt.xlabel(r'log($\nu_{syn}$ [Hz])', fontsize=14)
plt.ylabel('PL Index', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()




## Scatter plot PL Index vs. log(nu_syn) for different source classes
plt.subplots(figsize=(10,6))
plt.scatter(np.log10(catdf.loc[ catdf['CLASS']=='bll',  'nu_syn']), catdf.loc[ catdf['CLASS']=='bll', 'PL_Index'] , color='limegreen',  alpha=0.3, label='bll')
plt.scatter(np.log10(catdf.loc[ catdf['CLASS']=='fsrq', 'nu_syn']), catdf.loc[ catdf['CLASS']=='fsrq','PL_Index'] , color='darkorange', alpha=0.3, label='fsrq')
plt.xlabel(r'log($\nu_{syn}$ [Hz])', fontsize=14)
plt.ylabel('PL Index', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.show()





#############################  Scatter plot  con  errori  ###############################
## Scatter plot  PL Index vs. log(nu_syn) con errori for different source classes
plt.subplots(figsize=(10,6))
plt.errorbar(catdf.loc[ catdf['CLASS']=='bll',  'nu_syn'], catdf.loc[ catdf['CLASS']=='bll', 'PL_Index'], 
             yerr=catdf.loc[ catdf['CLASS']=='bll',  'Unc_PL_Index'],
             fmt='o', color='limegreen',  alpha=0.3, label='bll')
plt.errorbar(catdf.loc[ catdf['CLASS']=='fsrq',  'nu_syn'], catdf.loc[ catdf['CLASS']=='fsrq', 'PL_Index'], 
             yerr=catdf.loc[ catdf['CLASS']=='fsrq',  'Unc_PL_Index'],
             fmt='o', color='darkorange',  alpha=0.3, label='fsrq')

plt.xlabel(r'$\nu_{syn}$ [Hz]', fontsize=14)
plt.ylabel('PL Index', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.xscale('log')
plt.show()




#############################  Istogrammi  #####################################

# Istogramma PL_Index
plt.subplots(figsize=(10,6))
plt.hist(catdf.loc[ catdf['CLASS']=='bll', 'PL_Index'], bins=50, range=(1,4), color='limegreen',  alpha=1.0, label='bll')
plt.hist(catdf.loc[ catdf['CLASS']=='fsrq','PL_Index'], bins=50, range=(1,4), color='darkorange', alpha=0.4, label='fsrq')
plt.xlabel('PL Index', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.show()


# Istogramma nu_syn
plt.subplots(figsize=(10,6))
plt.hist(np.log10(catdf.loc[ catdf['CLASS']=='bll',  'nu_syn']), bins=50, range=(10,20), color='limegreen',  alpha=1.0, label='bll')
plt.hist(np.log10(catdf.loc[ catdf['CLASS']=='fsrq', 'nu_syn']), bins=50, range=(10,20), color='darkorange', alpha=0.4, label='fsrq')
plt.xlabel(r'log($\nu_{syn}$ [Hz])', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.show()






