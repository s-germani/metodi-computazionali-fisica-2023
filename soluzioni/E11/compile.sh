# Compilazione per libreria condivisa serie
gcc -o libserie.so  -shared serie.c

# Compilazione per libreria condivisa mycamera
gcc -o libmycamera.so   -shared mycamera.c  -lcurl


