//////////////////////////////////////////////////////
// S. Germani (stefano.germani@unipg.it)            //
//                                                  //
// Universià degli Studi di Perugia                 //
// Corso di Metodi Computazionali per la Fisica     //
//--------------------------------------------------//
// Esercitazione  11 - C e Python:                  //
//                                                  //
//   Definizione della libreria  serie              //
//    come  libreria condivisa                      //
//    per il calcolo della successione di Fibonacci //
//                                                  //
//   per compilare creando il file libserie.so:     //
//     gcc -o libserie.so  -shared serie.c          //
//////////////////////////////////////////////////////

#include <stdio.h>
#include <math.h>

double fibonacci(int n);


double fibonacci(int n){
  
  if(n>2){
    double vm1 = 1;
    double vm2 = 0;

    double vv;
      
    int i = 2;
    for(i=3; i<=n; i++){
      vv = vm2+vm1;
      vm2 = vm1;
      vm1 = vv;
    }
    return vm1/vm2;

  } else
    return 1;
}


