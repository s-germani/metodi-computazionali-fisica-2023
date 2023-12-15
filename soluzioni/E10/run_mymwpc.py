#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 10 - Metodi Monte Carlo:            #
#                                                   #
#   Script che utilizza le classi myMWPC e myMWPCev #
#     per simulare una Camera Proporzionale a       #
#     Molti Fili                                    #
#                                                   #
#####################################################


import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import time

import mymwpc, mymwpcev


def run():

    camera = mymwpc.myMWPC(su=1e-4, sf=5e-5, nr=1e4)
    
    camera_events = np.empty(0)
    
    for i in tqdm(range(1000)):
        npc, nr, pos, dt = camera.simulate_track()

        #print(npc, dt)
        camera_events = np.append( camera_events, mymwpcev.myMWPCev( npc, len(dt), pos, dt ) )

        #print(camera_events[-1]._nr / camera_events[-1]._np )
        
                                   

    positions  = np.empty(0)
    primaries  = np.empty(0)
    detections = np.empty(0)
    dt_first   = np.empty(0)
    dt_mean    = np.empty(0)
    
    for ce in camera_events:
        positions  = np.append( positions,  ce._pos)
        primaries  = np.append( primaries,  ce._np)
        detections = np.append( detections, ce._nr)
        dt_first   = np.append( dt_first,   ce._dt_first)
        dt_mean    = np.append( dt_mean,    ce._dt_mean)
    #print(camera_events._np[0])

    mask = primaries == 0 
    eff  = detections / primaries


    plt.hist(positions, bins=20, range=(-0.5, 0.5))
    plt.xlabel('Primary Position [cm]')
    plt.ylabel('entries / bin ')
    plt.show()

    plt.hist(primaries, bins=15, range=(0,15))
    plt.xlabel('Priamrie pairs')
    plt.ylabel('entries / bin ')
    plt.show()


    plt.hist(detections, bins=15, range=(0,15))
    plt.xlabel('Detected electrons')
    plt.ylabel('entries / bin ')
    plt.show()


    plt.hist(primaries,  bins=15, range=(0,15),            label='Primary')
    plt.hist(detections, bins=15, range=(0,15), alpha=0.6, label='Detected')
    plt.xlabel('Charges')
    plt.ylabel('entries / bin ')
    plt.legend()
    plt.show()

    plt.hist(np.log10(dt_mean),  range=(-12, -6), bins=48, alpha=1, label='mean')
    plt.hist(np.log10(dt_first), range=(-12, -6), bins=48, alpha=0.6, label='first')
    plt.xlabel(r'log($t$)')
    plt.ylabel('entries / bin ')
    plt.legend()
    plt.show()


    
    plt.hist(eff*100, bins=50)
    plt.xlabel(r'$\varepsilon$ (%)')
    plt.ylabel('entries / bin ')
    #plt.legend()
    plt.show()


    detected_tracks = np.count_nonzero(eff) 
    
    tracks_eff  = detected_tracks/len(camera_events)

    tracks_effe = np.sqrt( tracks_eff*(1-tracks_eff)/len(camera_events) )
    

    print('Eff = {:.2f} +- {:.2f}'.format(tracks_eff*100, tracks_effe*100) )










if __name__ == "__main__":

    run()
