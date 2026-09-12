#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_NAME_LENGTH 21

typedef struct {
    char name[MAX_NAME_LENGTH];
    int id;
} Pokemon;

int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    
    Pokemon pokemons[n + 1];
    for (int i = 1; i <= n; i++) {
        scanf("%s", pokemons[i].name);
        pokemons[i].id = i;
    }
    
    for (int i = 0; i < m; i++) {
        char q[MAX_NAME_LENGTH];
        scanf("%s", q);
        if (isdigit(q[0])) {
            int id = atoi(q);
            printf("%s\n", pokemons[id].name);
        } else {
            for (int j = 1; j <= n; j++) {
                if (strcmp(q, pokemons[j].name) == 0) {
                    printf("%d\n", pokemons[j].id);
                    break;
                }
            }
        }
    }
    return 0;
}
