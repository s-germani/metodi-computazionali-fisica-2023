////////////////////////////////////////////////////////////////////////////////////////////
// S. Germani (stefano.germani@unipg.it)                                                  //
//                                                                                        //
// Universià degli Studi di Perugia                                                       //
// Corso di Metodi Computazionali per la Fisica                                           //
//----------------------------------------------------------------------------------------//
// Esercitazione  11 - C e Python:                                                        //
//                                                                                        //
//   Codice per creare la libreria condivisa libmycamera.so                               //
//       che emula la lettura di una fotocamera fornendo                                  //  
//       una immagine sotto forma di buffer di bytes (char)                               //
//                                                                                        //
//       - dimensioni immagine:  1536 * 1024  pixel                                       //
//       - width  = 1536                                                                  //
//       - height = 1024                                                                  //
//       - 2 bytes / pixel                                                                //
//       - bytes totali immagine: 1536 * 1024 * 2                                         //
//                                                                                        //
//       Estratto dalla documentazopne della camera:                                      //
//         ...                                                                            //
//         - bottom left pixel's lower byte is located at buffer[0] and higher byte is    //
//              at buffer[1]                                                              //
//         - first line has width = 1536 * 2 (bytes) -> bottom right pixel is located     //  
//              at buffer[3070] and buffer[3071] (width * 2 - 2 and width * 2 - 1)        //
//         - top left pixel is at buffer[((height - 1) * width * 2] and                   // 
//              buffer[(height - 1) * width * 2 + 1)]                                     //
//         - top right pixel is at buffer[((height - 1) * width * 2 + width * 2 - 2] and  //
//              buffer[(height - 1) * width * 2 + width * 2 - 1)]                         //
//         ...                                                                            //
//                                                                                        //
//       Per compilare e produree la libreria condivisa:                                  //
//           gcc -o libmycamera.so   -shared mycamera.c  -lcurl                           //
//                                                                                        //
////////////////////////////////////////////////////////////////////////////////////////////
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <malloc.h>

struct MemoryStruct {
  char *memory;
  size_t size;
};

static size_t
WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  size_t realsize = size * nmemb;
  struct MemoryStruct *mem = (struct MemoryStruct *)userp;
 
  char *ptr = realloc(mem->memory, mem->size + realsize + 1);
  if(!ptr) {
    /* out of memory! */
    //printf("not enough memory (realloc returned NULL)\n");
    return 0;
  }
 
  mem->memory = ptr;
  memcpy(&(mem->memory[mem->size]), contents, realsize);
  mem->size += realsize;
  mem->memory[mem->size] = 0;
 
  return realsize;
}

int read_camera(char *buffer){

  
  CURL *curl_handle;
  CURLcode res;

  size_t imsize = 0;
  struct MemoryStruct chunk;
  
  chunk.memory = malloc(1);  /* will be grown as needed by the realloc above */
  chunk.size = 0;    /* no data at this point */
 
  curl_global_init(CURL_GLOBAL_ALL);
 
  /* init the curl session */
  curl_handle = curl_easy_init();
 
  /* specify URL to get */
  curl_easy_setopt(curl_handle, CURLOPT_URL, "https://raw.githubusercontent.com/s-germani/metodi-computazionali-fisica-2023/main/dati/c_e_python/myimage.txt");
 
  /* send all data to this function  */
  curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
 
  /* we pass our 'chunk' struct to the callback function */
  curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);
 
  /* some servers do not like requests that are made without a user-agent
     field, so we provide one */
  curl_easy_setopt(curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0");
 
  /* get it! */
  res = curl_easy_perform(curl_handle);

   
  /* check for errors */
  if(res != CURLE_OK) {
    printf("curl_easy_perform() failed: %s\n",
	   curl_easy_strerror(res));
  }
  else {
    /*
     * Now, our chunk.memory points to a memory block that is chunk.size
     * bytes big and contains the remote file.
     */

    imsize = chunk.size;
    // Copy chunk.memory into utput buffer
    memcpy(buffer, chunk.memory, chunk.size);	
  }
 
  /* cleanup curl stuff */
  curl_easy_cleanup(curl_handle);
 
  free(chunk.memory);
 
  /* we are done with libcurl, so clean it up */
  curl_global_cleanup();


  /*  

  // ------------  DEBUG BUFFER  --------------------------------------------------------------
  int width  = 1536;
  int height = 1024;
  int photo[1024][1536];

  int x = -1;
  int y = -1;
  
  int pixel_value = -1;
	
  
  for(int i=0; i<imsize; i+=2){
    x = (i / 2) % width;
    y = (i / 2) / width; 
    pixel_value = (unsigned char)buffer[i] + ((unsigned char)buffer[i+1] << 8);
    photo[y][x] = pixel_value;

    printf( "%d  %d  -  %d\n", (unsigned char)buffer[i], (unsigned char)buffer[i+1], pixel_value);   
  } 
  // -------------------------------------------------------------------------------------------------
  */
  
  
  return 0;
}




