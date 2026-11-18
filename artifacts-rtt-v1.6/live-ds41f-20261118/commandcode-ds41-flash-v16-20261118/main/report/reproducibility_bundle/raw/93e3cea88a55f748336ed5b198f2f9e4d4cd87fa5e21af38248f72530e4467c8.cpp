#include <iostream>
#include <functional>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    const int full = (1 << n) - 1;
    long long ans = 0;

    std::function<void(int, int, int)> solve = [&](int cols, int diag1, int diag2) {
        if (cols == full) {
            ++ans;
            return;
        }

        int available = ~(cols | diag1 | diag2) & full;
        while (available) {
            int bit = available & -available;
            available -= bit;
            solve(cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1);
        }
    };

    solve(0, 0, 0);
    std::cout << ans << '\n';

    return 0;
}