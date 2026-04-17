#include <stdio.h>

int has666(int x) {
    int consecutive = 0;
    if (x == 0) return 0;
    while (x > 0) {
        if (x % 10 == 6) {
            consecutive++;
            if (consecutive >= 3) return 1;
        } else {
            consecutive = 0;
        }
        x /= 10;
    }
    return 0;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    int count = 0;
    int value = 665;
    while (count < n) {
        ++value;
        if (has666(value)) {
            ++count;
        }
    }

    printf("%d\n", value);
    return 0;
}
