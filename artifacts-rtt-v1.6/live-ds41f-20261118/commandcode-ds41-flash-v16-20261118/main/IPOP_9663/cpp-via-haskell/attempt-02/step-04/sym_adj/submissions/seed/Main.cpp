#include <iostream>
#include <functional>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    int full = (1 << n) - 1;

    std::function<int(int, int, int, int)> go =
        [&](int r, int cols, int d1, int d2) -> int {
            if (r == n) return 1;

            int avail = full & ~(cols | d1 | d2);
            int acc = 0;

            while (avail) {
                int b = avail & -avail;
                avail ^= b;

                acc += go(
                    r + 1,
                    cols | b,
                    ((d1 | b) << 1) & full,
                    (d2 | b) >> 1
                );
            }

            return acc;
        };

    std::cout << go(0, 0, 0, 0) << '\n';
    return 0;
}