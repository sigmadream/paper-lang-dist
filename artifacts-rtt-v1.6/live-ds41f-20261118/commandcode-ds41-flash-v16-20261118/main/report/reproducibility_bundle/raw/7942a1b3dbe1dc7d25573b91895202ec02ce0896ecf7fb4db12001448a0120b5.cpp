#include <iostream>
#include <string>

void hanoi(int n, int from, int via, int to, std::string& out) {
    if (n == 1) {
        out += std::to_string(from);
        out += ' ';
        out += std::to_string(to);
        out += '\n';
        return;
    }
    hanoi(n - 1, from, to, via, out);
    out += std::to_string(from);
    out += ' ';
    out += std::to_string(to);
    out += '\n';
    hanoi(n - 1, via, from, to, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    if (n > 0) {
        long long moves = (1LL << n) - 1;
        std::string out;
        out.reserve(static_cast<size_t>(moves) * 4 + 32);
        out += std::to_string(moves);
        out += '\n';
        hanoi(n, 1, 2, 3, out);
        std::cout << out;
    }

    return 0;
}