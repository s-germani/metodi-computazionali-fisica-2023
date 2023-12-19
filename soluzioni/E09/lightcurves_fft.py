#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 9 - Trasformate di Fourier:         #
#                                                   #
#   FFT curve di luce Fermi-LAT                     #
#                                                   #
#####################################################

import numpy as np
import pandas as pd
from scipy import constants, fft, optimize
import matplotlib.pyplot  as plt

import argparse

#####################################################################
#      Funzione per fit Spettro di Potenza                          #         
#####################################################################


def noisef(f, N, beta):
    """
    Funzione per fit Spettro Potenza di diversi tipi di rumore

    f    : frequenze
    N    : normalizzazione
    beta : esponente per dipendenza da frequenza

    return N/f^beta
    """
    
    return N/f**beta



#####################################################################
#      Funzione per gestione opzioni (argparse)                     #
#####################################################################

def parse_arguments():

    parser = argparse.ArgumentParser(description='Plot and fit noise data.',
                                     usage      ='python3 lightcurve_fft.py  --option')
    parser.add_argument('--lc',   action='store_true',         help='Plot input Light Curves')
    parser.add_argument('--psplot',    action='store_true',    help='FFT and Power Spectrum plots')
    parser.add_argument('--psfit',     action='store_true',    help='Power Spectrum Fit')
    
    return  parser.parse_args()



#####################################################################
#      Funzione principale per calcolo FFT                          #         
#####################################################################

def lightcurves_fft():



    args = parse_arguments()



    #---------------------------------------------------------------#
    #              Dictionary con informazioni sorgenti e file      #
    #---------------------------------------------------------------#

    source_dict = { 'Bl Lac'       : { 'file' : '4FGL_J2202.7+4216_weekly_9_15_2023_mcf.csv',   'class': 'BLL'  },
                    'S5 0716+71'   : { 'file' : '4FGL_J0721.9+7120_weekly_9_15_2023_mcf.csv',   'class': 'BLL'  },
                    'PKS 0426-380' : { 'file' : '4FGL_J0428.6-3756_weekly_9_15_2023_mcf.csv',   'class': 'BLL'  },                    
                    '3C 279'       : { 'file' : '4FGL_J1256.1-0547_weekly_9_15_2023_mcf.csv',   'class': 'FSRQ' },
                    '3C 454.3'     : { 'file' : '4FGL_J2253.9+1609_weekly_9_15_2023_mcf.csv',   'class': 'FSRQ' },                    
                    'CTA 102'      : { 'file' : '4FGL_J2232.6+1143_weekly_9_15_2023_mcf.csv',   'class': 'FSRQ' } }                    
                
    
    
    

    #---------------------------------------------------------------#
    #  Lettura files di dati  e aggiunta dataframe a dictionary     #
    #---------------------------------------------------------------#

    for source in source_dict:

        dfsource = pd.read_csv( source_dict[source]['file'] )
        source_dict[source].update( {'df' : dfsource } ) 
        
    

    #---------------------------------------------------------------#
    #              Grafico segnali di input                         #
    #---------------------------------------------------------------#
    if args.lc == True:
        
        fig,ax = plt.subplots(figsize=(9,6))
        for source in source_dict:
            plt.plot(source_dict[source]['df']['Julian Date'], source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],  label=source)

        plt.legend()
        plt.xlabel('Julian Date')
        plt.ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)')
        plt.show()




        fig,ax = plt.subplots(6,1,figsize=(10,11), sharex=True)
        ia = 0
        
        for source in source_dict:

            sc = 'darkorange'
            if source_dict[source]['class'] == 'FSRQ':
                sc = 'limegreen'
                
            ax[ia].plot(source_dict[source]['df']['Julian Date'], source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],  color = sc, label=source) 
            ax[ia].legend()            
            ax[ia].set_ylabel('photons cm-2 s-1')
            ia+=1
            
        ax[ia-1].set_xlabel('Julian Date')
        plt.show()


    #---------------------------------------------------------------#
    #              Calcolo e grafici FFT                            #
    #---------------------------------------------------------------#
    if args.psplot == True or  args.psfit == True:


        #-----------------------------------------------------------#
        #              Calcolo FFT                                  #
        #-----------------------------------------------------------#

        for source in source_dict:            

            # Delta t
            dt = source_dict[source]['df']['Julian Date'][1]-source_dict[source]['df']['Julian Date'][0]

            # FFT e frequenze
            cc  = fft.fft(source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'].values)
            ff  = fft.fftfreq(len(cc), d=dt)

            # Aggiunta risulatti FFT a dictionary con info sorgenti
            source_dict[source].update(  { 'c' : cc, 'freq' : ff })

        #print(source_dict)
        
        #---------------------------------------------------------------#
        #                     Grafico PS                                #
        #---------------------------------------------------------------#
        if args.psplot == True:

            fig,ax = plt.subplots(figsize=(9,6))

            for source in source_dict:
                tmp_len = len(source_dict[source]['c'])//2
                plt.plot( source_dict[source]['freq'][:tmp_len], np.absolute(source_dict[source]['c'][:tmp_len])**2,  label=source)

            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.legend()
            plt.show()
            
            
            fig,ax = plt.subplots(figsize=(9,6))
            
            for source in source_dict:
                sc = 'darkorange'
                if source_dict[source]['class'] == 'FSRQ':
                    sc = 'limegreen'

                tmp_len = len(source_dict[source]['c'])//2
                plt.plot( source_dict[source]['freq'][:tmp_len], np.absolute(source_dict[source]['c'][:tmp_len])**2,  color=sc, label=source)

            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.legend()
            plt.show()




            fig,ax = plt.subplots(figsize=(9,6))
            
            for source in source_dict:            
                tmp_len = len(source_dict[source]['c'])//2
                ps0 = np.absolute(source_dict[source]['c'][0])**2
                plt.plot( source_dict[source]['freq'][:tmp_len], (np.absolute(source_dict[source]['c'][:tmp_len])**2)/ps0,  label=source)

            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.legend()
            plt.show()



            
            fig,ax = plt.subplots(figsize=(9,6))
            
            for source in source_dict:            

                sc = 'darkorange'
                if source_dict[source]['class'] == 'FSRQ':
                    sc = 'limegreen'

                tmp_len = len(source_dict[source]['c'])//2
                ps0 = np.absolute(source_dict[source]['c'][0])**2                
                plt.plot( source_dict[source]['freq'][:tmp_len], (np.absolute(source_dict[source]['c'][:tmp_len])**2)/ps0,  color=sc, label=source)

            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.legend()
            plt.show()



        #---------------------------------------------------------------#
        #              Fit PS                                           #
        #---------------------------------------------------------------#

        if args.psfit == True: 

            fig,ax = plt.subplots(6,1,figsize=(10,11), sharex=True)
            ia = 0
        
            for source in source_dict:

                tmp_len = len(source_dict[source]['c'])//2
                pv, pc = optimize.curve_fit(noisef , source_dict[source]['freq'][2:tmp_len], np.absolute(source_dict[source]['c'][2:tmp_len])**2, p0=[1e-16, 2])
                print('Parameters Fit Sample 1', pv)

                sc = 'darkorange'
                if source_dict[source]['class'] == 'FSRQ':
                    sc = 'limegreen'
                     
                
                ax[ia].plot( source_dict[source]['freq'][:tmp_len], np.absolute(source_dict[source]['c'][:tmp_len])**2,  color=sc, label=source)
                ax[ia].plot( source_dict[source]['freq'][:tmp_len], noisef(source_dict[source]['freq'][:tmp_len], pv[0], pv[1] ), color='darkred'   )
                #ax[ia].plot( source_dict[source]['freq'][1:tmp_len], noisef(source_dict[source]['freq'][1:tmp_len], 1e-16, 2 ), color='darkred'   )
                ax[ia].legend()            
                ax[ia].set_ylabel('')
                ax[ia].set_xscale('log')
                ax[ia].set_yscale('log')

                ax[ia].text(0.1, 0.1, r'$\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv[1], np.sqrt(pc[1,1])), fontsize=14, transform=ax[ia].transAxes, color=sc)
                ia+=1
                    
            ax[ia-1].set_xlabel('f [Hz]')
            plt.show()


            
"""
            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2,  color='limegreen')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.show()


            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2,  color='orange')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.show()


            # Grafico PS Campion1 1,2,3
            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2,        color='cyan')
            plt.plot( f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2,        color='limegreen')
            plt.plot( f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2,        color='orange')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.show()


        #---------------------------------------------------------------#
        #              Fit PS                                           #
        #---------------------------------------------------------------#
    
        if args.psfit == True: 

            # Fit Sample 1
            pv1, pc1 = optimize.curve_fit(noisef , f1[2:len(c1)//2], np.absolute(c1[2:len(c1)//2])**2, p0=[1, 1])
            print('Parameters Fit Sample 1', pv1)

            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f1[:len(c1)//2],  np.absolute(c1[:len(c1)//2])**2,           color='cyan')
            plt.plot( f1[1:len(c1)//2], noisef(f1[1:len(c1)//2], pv1[0], pv1[1] ), color='darkcyan'   )
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.text(0.1, 0.1, r'Sample 1 -  $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv1[1], np.sqrt(pc1[1,1])), fontsize=14, transform=ax.transAxes, color='darkcyan' )
            plt.show()



            # Fit Sample 2
            pv2, pc2 = optimize.curve_fit(noisef , f2[5:len(c2)//2], np.absolute(c2[5:len(c2)//2])**2, p0=[1, 1])
            print('Parameters Fit Sample 2', pv2)

            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f2[:len(c2)//2],  np.absolute(c2[:len(c2)//2])**2,           color='limegreen')
            plt.plot( f2[1:len(c2)//2], noisef(f2[1:len(c2)//2], pv2[0], pv2[1] ), color='darkgreen')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.text(0.1, 0.1, r'Sample 2 -  $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv2[1], np.sqrt(pc2[1,1])), fontsize=14, transform=ax.transAxes, color='darkgreen' )
            plt.show()



            # Fit Sample 3
            pv3, pc3 = optimize.curve_fit(noisef , f3[5:len(c3)//2], np.absolute(c3[5:len(c3)//2])**2, p0=[1, 1])
            print('Parameters Fit Sample 3', pv3)

            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f3[:len(c3)//2],  np.absolute(c3[:len(c3)//2])**2,           color='orange')
            plt.plot( f3[1:len(c3)//2], noisef(f3[1:len(c3)//2], pv3[0], pv3[1] ), color='darkred'   )
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.text(0.1, 0.1, r'Sample 3 -  $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv3[1], np.sqrt(pc3[1,1])), fontsize=14, transform=ax.transAxes, color='darkred' )
            plt.show()



            #---------------------------------------------------------------#
            #              Grafico Finale                                   #
            #---------------------------------------------------------------#
            
            # Grafico PS Campion1 1,2,3 con Fit
            plt.style.use('dark_background')
            fig,ax = plt.subplots(figsize=(9,6))
            plt.plot( f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2, color='white',  label=r'Sample 1 - $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv1[1], np.sqrt(pc1[1,1])) )
            plt.plot( f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2, color='pink'  , label=r'Sample 2 - $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv2[1], np.sqrt(pc2[1,1])) )
            plt.plot( f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2, color='tomato', label=r'Sample 3 - $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv3[1], np.sqrt(pc3[1,1])) )

            plt.plot( f1[1:len(c1)//2], noisef(f1[1:len(c1)//2], pv1[0], pv1[1] ), color='slategray' )
            plt.plot( f2[1:len(c2)//2], noisef(f2[1:len(c2)//2], pv2[0], pv2[1] ), color='magenta'   )
            plt.plot( f3[1:len(c3)//2], noisef(f3[1:len(c3)//2], pv3[0], pv3[1] ), color='darkred'   )

            plt.legend(fontsize=14, frameon=False)
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('f [Hz]')
            plt.show()
"""


if __name__ == "__main__":

    lightcurves_fft()
