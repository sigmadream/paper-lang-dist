#include <stdio.h>
#include <string.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    int count = 0;
    int value = 665;
    char s[32];

    while (count < n) {
        ++value;
        sprintf(s, "%d", value);
        if (strstr(s, "666") != NULL) {
            ++count;
        }
    }

    printf("%d\n", value);
    return 0;
}
