#include <iostream>
#include <string>

long long countQueens(int n) {
    int full = (1 << n) - 1;

    auto go = [&](auto&& self, int r, int cols, int diag1, int diag2) -> long long {
        if (r == n) return 1;

        long long acc = 0;
        int available = full & ~(cols | diag1 | diag2);

        while (available != 0) {
            int bit = available & -available;
            available ^= bit;

            int nextCols = cols | bit;
            int nextDiag1 = ((diag1 | bit) << 1) & full;
            int nextDiag2 = (diag2 | bit) >> 1;

            acc += self(self, r + 1, nextCols, nextDiag1, nextDiag2);
        }

        return acc;
    };

    return go(go, 0, 0, 0, 0);
}

int main() {
    std::string input;
    if (std::cin >> input) {
        int n = std::stoi(input);
        std::cout << countQueens(n) << '\n';
    }
    return 0;
}