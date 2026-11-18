#include <cstdio>
#include <iostream>

int main() {
    long long N;
    if (!(std::cin >> N)) return 0;
    if (N >= 0) {
        for (long long i = 0; i <= N; ++i) {
            long long x = i;
            long long c = 0;
            while (x > 0) {
                c += x & 1;
                x >>= 1;
            }
            if (i > 0) std::putchar(' ');
            std::printf("%lld", c);
        }
    }
    std::putchar('\n');
    return 0;
}