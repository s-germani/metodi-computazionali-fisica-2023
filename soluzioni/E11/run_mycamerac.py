#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione  11 - C e Python:                   #
#                                                   #
#   Utilizzo della Classe myCamera                  #
#    che sfrutta la libreria condivisa mycamera     #
#####################################################

import argparse

import mycamerac


def parse_arguments():

    parser = argparse.ArgumentParser(description='Read camera data through  myCameraO class defined in the mycamerao mudule and using the mycamera shared library',
                                     usage      ='python3 run_mycamerao.py  --opzione [--opzione2 --opzione3 ... --opzioneN] ')
    parser.add_argument('--read_camera',    action='store_true',    help='Acquisisce immagine dalla Camera')
    parser.add_argument('--image_info',     action='store_true',    help='Stampa informazioni sull\' immagine acquisita')
    parser.add_argument('--show_image',     action='store_true',    help='Mostra l\'immagine acquisita')
    parser.add_argument('--no_cbar',        action='store_true',    help='Mostra l\'immagine senza barra di colori')
    parser.add_argument('--norm',           action='store',         default='log', help='Imposta l\'opzione di normalizzazione dell\'immagine (default=\'log\'')
    parser.add_argument('--cmap',           action='store',         default='gray', help='Imposta la mappa di colori dell\'immagine (default=\'gray\'')

    parser.add_argument('--image_file',     action='store',         default='', help='File dove salvare l\'immagine (default: immagine nonsalvata') 
    return  parser.parse_args()


def run():

    args = parse_arguments()
    
    myc = mycamerac.myCamera()
    myc.set_image_file(args.image_file)
        
    if args.read_camera == True:
        myc.read_camera()

    if args.image_info == True:
        print(myc)
        
    if args.no_cbar == True:
        myc.set_colorbar(False)
        
    if args.show_image == True:
        myc.show_image(nrm=args.norm, cm=args.cmap)
         
    elif args.image_file != '':
        myc.save_image(nrm=args.norm, cm=args.cmap)

        

    




if __name__ ==  "__main__":
    run()



