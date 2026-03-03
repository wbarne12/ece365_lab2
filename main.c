#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// This is the max amount of args 😀😀
// Will return in the sequence of [sets, blocks, size, trace, policy]
// If there is no arg for the first 3, they will contain -1
// For trace and policy, will contain NO_INPUT
// All elements are c-style strings
// Returns NULL if something gets messed up, say not enough args
char **parse_args(int argc, char*argv[]) {
    
    char **args = malloc(sizeof(char *) * 5); 

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--sets") == 0) {
            if (i+1 > argc) {
                return NULL;
            }
            args[1] = strdup(argv[i+1]);
        } else if (strcmp(argv[i], "--blocks") == 0) {
            if (i+1 > argc) {
                return NULL;
            }
            args[2] = strdup(argv[i+1]);
        } else if (strcmp(argv[i], "--size") == 0) {
            if (i+1 > argc) {
                return NULL;
            }
            args[3] = strdup(argv[i+1]);
        } else if (strcmp(argv[i], "--trace") == 0) {
            if (i+1 > argc) {
                return NULL;
            }
            args[4] = strdup(argv[i+1]);
        } else if (strcmp(argv[1], "--policy") == 0) {
            if (i+1 > argc) {
                return NULL;
            }
            args[5] = strdup(argv[i+1]);
        } else {
        }
     }

}

int main(int argc, char *argv[]) {
    printf("farts\n");

    return 0;
} 