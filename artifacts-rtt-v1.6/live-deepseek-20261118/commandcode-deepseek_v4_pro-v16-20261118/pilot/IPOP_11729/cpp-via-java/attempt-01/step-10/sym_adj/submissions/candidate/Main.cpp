#include <iostream>
#include <string>

void hanoi(int n, int from, int aux, int to, std::string& out) {
    if (n == 1) {
        out += std::to_string(from);
        out += ' ';
        out += std::to_string(to);
        out += '\n';
        return;
    }
    hanoi(n - 1, from, to, aux, out);
    out += std::to_string(from);
    out += ' ';
    out += std::to_string(to);
    out += '\n';
    hanoi(n - 1, aux, from, to, out);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    std::cin >> n;

    int moves = (1 << n) - 1;
    std::string out;
    out.reserve(static_cast<size_t>(moves) * 4 + 20);
    out += std::to_string(moves);
    out += '\n';

    hanoi(n, 1, 2, 3, out);

    std::cout << out;
    return 0;
}