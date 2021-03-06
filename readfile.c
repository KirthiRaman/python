#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// This file was originally created (the first source file to be created in solving the assignment)
// I usually try something in C and Python just for curiousity (I do not want to lose touch with C programming - sort
//  of my first programming language that I really felt like doing something)
char fname[] = "gamedata.txt";
char outputfname[] = "flight_paths.txt";
int start[5000], finish[5000], energy[5000];
int sort_index[5000];

int findStartIndex(int str, int fromhere){
   int i=fromhere;
   int found=0;
   int retval = -1;

   while ( i < 5000 && (found==0) ){
      if ( start[i] == str ) {
          found = 1;
          retval = i;
      }
      i++;
   }
   return retval;
}

void sortFinish(int largstr, FILE *outfile){
   int *numsortindex;
   numsortindex = malloc(sizeof(int)*largstr);
   int i=0, arindex;
   int fromstart = 0;
   int bitlist[5000];
   
   for(i=1; i<=largstr; i++)
      numsortindex[i] = 0;
   
   for(i=0; i<5000; i++){
      numsortindex[start[i]]  = 1;
      bitlist[i] = 0;
   }

   for(i=1;i<=largstr; i++){
      if ( numsortindex[i] > 0 ){
         fromstart=0;
         arindex = findStartIndex(i, fromstart);
         while ( arindex > -1 ){
            if ( bitlist[arindex] != 1){
               bitlist[arindex] = 1;
               fprintf(outfile,"%d %d %d\n",start[arindex], finish[arindex], energy[arindex]);
            }      
            fromstart = arindex+1;
            arindex = findStartIndex(i, fromstart);
            if ( arindex > 1) i++;
         }
      }
   }
}

void create_array() {
  FILE *inFile;
  FILE *outFile;
  int largstr=0, largstrIndex=0;
  int i=0, st, fin,en;
  int energyNojet;

  inFile = fopen(fname, "r");
  outFile = fopen(outputfname, "w");
  fscanf(inFile,"%d\n",&energyNojet);
  while (fscanf(inFile, "%d %d %d\n", &st,&fin,&en) != EOF) {
      start[i] = st;
      finish[i] = fin;
      if ( st > largstr ) { largstr = st; largstrIndex=i; }
      energy[i++] = en;
  }
  fclose(inFile);

  sortFinish(largstr, outFile);
  fprintf(outFile,"%d\n",energyNojet);
  printf("LargeStart = %d and index = %d\n",largstr, largstrIndex);
}


int main(int argc, char *argv[]) {
  create_array();
}
