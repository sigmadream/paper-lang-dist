#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_NAME_LENGTH 21

typedef struct {
    char name[MAX_NAME_LENGTH];
    int id;
} Pokemon;

int compare(const void *a, const void *b) {
    return ((Pokemon *)a)->id - ((Pokemon *)b)->id;
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    
    Pokemon pokemons[n + 1];
    for (int i = 1; i <= n; i++) {
        scanf("%s", pokemons[i].name);
        pokemons[i].id = i;
    }
    
    qsort(pokemons + 1, n, sizeof(Pokemon), compare);
    
    for (int i = 0; i < m; i++) {
        char q[MAX_NAME_LENGTH];
        scanf("%s", q);
        if (isdigit(q[0])) {
            int id = atoi(q);
            for (int j = 1; j <= n; j++) {
                if (pokemons[j].id == id) {
                    printf("%s\n", pokemons[j].name);
                    break;
                }
            }
        } else {
            for (int j = 1; j <= n; j++) {
                if (strcmp(pokemons[j].name, q) == 0) {
                    printf("%d\n", pokemons[j].id);
                    break;
                }
            }
        }
    }
    return 0;
}
