#include <stdio.h>
#include <string.h>

int main() {
    int n;
    scanf("%d", &n);

    int count = 0;
    int value = 665;
    while (count < n) {
        ++value;
        if (strstr((char*)&value, "666") != NULL) {
            ++count;
        }
    }

    printf("%d\n", value);
    return 0;
}
