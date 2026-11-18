#include <iostream>
#include <functional>

long long solve(int n) {
    int full = (1 << n) - 1;

    std::function<long long(int, int, int, int)> go =
        [&](int r, int cols, int d1, int d2) -> long long {
            if (r == n) return 1;

            long long total = 0;
            int avail = full & ~(cols | d1 | d2);

            while (avail) {
                int b = avail & -avail;
                avail ^= b;

                total += go(
                    r + 1,
                    cols | b,
                    ((d1 | b) << 1) & full,
                    (d2 | b) >> 1
                );
            }

            return total;
        };

    return go(0, 0, 0, 0);
}

int main() {
    int n;
    if (std::cin >> n) {
        std::cout << solve(n) << '\n';
    }
    return 0;
}