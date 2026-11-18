#include <cstdio>

static int popcount(int x) {
    if (x == 0) return 0;
    return (x & 1) + popcount(x >> 1);
}

int main() {
    int c;
    do {
        c = getchar();
    } while (c == ' ' || c == '\t' || c == '\n' || c == '\r');

    int N = 0;
    if (c != EOF) {
        while (c >= '0' && c <= '9') {
            N = N * 10 + (c - '0');
            c = getchar();
        }
    }

    if (N < 0) {
        putchar('\n');
        return 0;
    }

    for (int i = 0; i <= N; i++) {
        if (i > 0) putchar(' ');
        printf("%d", popcount(i));
    }
    putchar('\n');
    return 0;
}